#!/usr/bin/env python3
"""Deterministic pi Keysmith fixture emitting pi-keysmith.envelope.v1.

State comes from files under --pi-dir:
- missing pi_dir: not-installed (deploy blocked by pi-dir-missing)
- `.fixture-conflict`: conflict
- any `.keysmith-*` file: recovery-required (temp residue)
- `.pi-keysmith-manifest.json` whose `after` differs from SYSTEM.md: drift
- manifest matching SYSTEM.md: active-aligned

FIXTURE_LOCK_BUSY=1 makes a confirmed write fail with exit 5; FIXTURE_WRITE_FAILED=1 makes it
fail with exit 4 after leaving a temp file behind.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

VERSION = os.environ.get("FIXTURE_VERSION", "0.2.0")
MANIFEST = ".pi-keysmith-manifest.json"
PRESERVES = ["APPEND_SYSTEM.md", "AGENTS.md", "CLAUDE.md", "settings.json", "models.json"]


def flag(argv: list[str], name: str) -> str | None:
    if name in argv:
        idx = argv.index(name)
        if idx + 1 < len(argv):
            return argv[idx + 1]
    return None


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def node(path: Path) -> dict:
    if path.is_file():
        data = path.read_bytes()
        return {"kind": "regular", "path": str(path), "fingerprint": {"sha256": sha(data), "size": len(data)}}
    return {"kind": "missing", "path": str(path), "fingerprint": None}


def inspect(root: Path) -> dict:
    nodes = {"pi_dir": {"kind": "directory" if root.is_dir() else "missing", "path": str(root)}}
    for key, name in (("system", "SYSTEM.md"), ("manifest", MANIFEST), ("append_system", "APPEND_SYSTEM.md"), ("agents_md", "AGENTS.md"), ("claude_md", "CLAUDE.md")):
        nodes[key] = node(root / name)
    conflicts: list[str] = []
    drift: list[str] = []
    temps = sorted(p.name for p in root.glob(".keysmith-*")) if root.is_dir() else []
    manifest = None
    if root.is_dir():
        if (root / ".fixture-conflict").exists():
            conflicts.append("manifest-invalid")
        if (root / MANIFEST).is_file():
            manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
            if nodes["system"]["kind"] != "regular" or nodes["system"]["fingerprint"]["sha256"] != manifest["after"]:
                drift.append("system-fingerprint-mismatch")
    if not root.is_dir():
        state = "not-installed"
    elif conflicts:
        state = "conflict"
    elif temps:
        state = "recovery-required"
    elif manifest is None:
        state = "not-installed"
    elif drift:
        state = "drift"
    else:
        state = "active-aligned"
    deploy = list(conflicts)
    uninstall = list(conflicts)
    if not root.is_dir():
        deploy.append("pi-dir-missing")
        uninstall.append("pi-dir-missing")
    if temps:
        deploy.append("residue-present")
        uninstall.append("residue-present")
    if manifest is None:
        uninstall.append("not-installed")
    uninstall.extend(drift)
    return {
        "state": state,
        "recovery_required": state == "recovery-required",
        "nodes": nodes,
        "manifest": None,
        "drift": drift,
        "conflicts": conflicts,
        "residue": {"journals": [], "cleanup_markers": [], "temp_files": temps},
        "preserved_changed": [],
        "blockers": {"deploy": deploy, "uninstall": uninstall},
        "deployable": not deploy,
        "uninstall_ready": not uninstall,
    }


def token(operation: str, status: dict, prompt_sha: str | None) -> str:
    payload = {
        "operation": operation,
        "state": status["state"],
        "system": (status["nodes"]["system"]["fingerprint"] or {}).get("sha256"),
        "temps": status["residue"]["temp_files"],
        "prompt": prompt_sha,
    }
    return sha(json.dumps(payload, sort_keys=True).encode("utf-8"))


def emit(operation, root, ok, exit_code, status, plan=None, result=None, diagnostics=None, preview=True) -> int:
    target = {"pi_dir": str(root), "pi_dir_resolved": os.path.realpath(str(root)), "scope": "user"} if root else {}
    envelope = {
        "schema": "pi-keysmith.envelope.v1",
        "tool": "pi-keysmith",
        "version": VERSION,
        "operation": operation,
        "preview": preview,
        "apply": not preview,
        "ok": ok,
        "exit_code": exit_code,
        "target": target,
        "status": status,
        "plan": plan,
        "result": result,
        "diagnostics": diagnostics or [],
    }
    print(json.dumps(envelope, ensure_ascii=False))
    return exit_code


def diag(code: str) -> str:
    return f"{code}: fixture {code}"


def main(argv: list[str]) -> int:
    if "--version" in argv:
        print(f"pi-keysmith.py {VERSION}")
        return 0
    raw = flag(argv, "--pi-dir")
    if not raw:
        return emit(None, None, False, 2, None, diagnostics=[diag("pi-dir-required")])
    if not os.path.isabs(raw):
        return emit(None, None, False, 2, None, diagnostics=[diag("pi-dir-not-absolute")])
    root = Path(raw)
    yes = "--yes" in argv
    expected = flag(argv, "--expected-preview-token")
    if "--status" in argv:
        status = inspect(root)
        bad = status["state"] in ("conflict", "recovery-required")
        return emit("status", root, not bad, 1 if bad else 0, status, diagnostics=[diag(c) for c in status["conflicts"] + status["drift"]])
    if yes and expected is None:
        return emit(None, root, False, 2, None, diagnostics=[diag("preview-token-required")])
    if "--uninstall" in argv:
        operation = "uninstall"
    elif "--recover" in argv:
        operation = "recover"
    else:
        operation = "deploy"
    prompt = None
    data = b""
    if operation == "deploy":
        source = flag(argv, "--file")
        data = Path(source).read_bytes() if source else b"fixture-pi\n"
        prompt = {"name": flag(argv, "--name") or "system-prompt", "source": "file" if source else "builtin", "sha256": sha(data), "size": len(data)}
    status = inspect(root)
    if operation == "deploy":
        blockers = status["blockers"]["deploy"]
        writes = [{"path": "SYSTEM.md", "action": "replace" if status["nodes"]["system"]["kind"] == "regular" else "create"}, {"path": MANIFEST, "action": "create"}]
    elif operation == "uninstall":
        blockers = status["blockers"]["uninstall"]
        writes = [{"path": "SYSTEM.md", "action": "remove"}, {"path": MANIFEST, "action": "archive", "archive": f"{MANIFEST}.archived"}]
    else:
        blockers = list(status["conflicts"]) + ([] if root.is_dir() else ["pi-dir-missing"])
        writes = [{"path": name, "action": "remove"} for name in status["residue"]["temp_files"]]
    plan = {
        "confirmation_token": None if blockers else token(operation, status, prompt and prompt["sha256"]),
        "blockers": blockers,
        "writes": [] if blockers else writes,
        "preserves": PRESERVES,
    }
    if prompt:
        plan["prompt"] = prompt
    if not yes:
        return emit(operation, root, not blockers, 1 if blockers else 0, status, plan, diagnostics=[diag(c) for c in blockers])
    if os.environ.get("FIXTURE_LOCK_BUSY") == "1":
        return emit(operation, root, False, 5, status, plan, diagnostics=[diag("lock-busy")])
    if expected != token(operation, status, prompt and prompt["sha256"]):
        return emit(operation, root, False, 3, status, plan, diagnostics=[diag("preview-token-mismatch")])
    if blockers:
        return emit(operation, root, False, 1, status, plan, diagnostics=[diag(c) for c in blockers])
    if os.environ.get("FIXTURE_WRITE_FAILED") == "1":
        (root / ".keysmith-fixture.tmp").write_bytes(b"partial")
        return emit(operation, root, False, 4, inspect(root), plan, diagnostics=[diag("write-failed")])
    if operation == "deploy":
        (root / "SYSTEM.md").write_bytes(data)
        (root / MANIFEST).write_text(json.dumps({"after": sha(data)}), encoding="utf-8")
    elif operation == "uninstall":
        (root / "SYSTEM.md").unlink()
        (root / MANIFEST).unlink()
    else:
        for name in status["residue"]["temp_files"]:
            (root / name).unlink()
    after = inspect(root)
    result = {
        "transaction_id": "0" * 32,
        "applied": True,
        "system_sha256": (after["nodes"]["system"]["fingerprint"] or {}).get("sha256"),
        "manifest_sha256": (after["nodes"]["manifest"]["fingerprint"] or {}).get("sha256"),
        "cleaned": status["residue"]["temp_files"] if operation == "recover" else [],
    }
    return emit(operation, root, True, 0, after, plan, result, preview=False)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
