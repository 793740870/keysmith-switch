# Adapter CLI 映射

统一 command 到五个钉选 CLI 的 argv。所有参数均为独立 argv 元素。

## Claude Code (`third_party/keysmith/claude/claude-instruct.py`)

| 统一命令 | argv |
| --- | --- |
| version | `--version` |
| status | `status --scope <scope> [--project-dir <abs>] [--runtime] --json` |
| plan-activate | `install --scope <scope> --file <abs.md> --name <safe> [--project-dir <abs>] [--runtime] [--append-file <abs.md>] [--max-tokens <n>] --json` |
| activate | 同上 + `--yes`。`--runtime` 只在 user scope；`--max-tokens` 是正整数 |
| plan-deactivate | `uninstall --scope <scope> [--project-dir <abs>] --json` |
| deactivate | 同上 + `--yes` |
| doctor | `doctor --json` |
| recover | `recover --scope <scope> [--project-dir <abs>] --json` 确认后加 `--yes` |
| backups | `backups --scope <scope> [--project-dir <abs>] --json`。只读，没有 `--yes` |
| restore | `restore --target <abs> --backup <name> [--scope <scope>] [--project-dir <abs>] --json`。预览在前，确认后加 `--yes` |

stdout JSON schema: `claude-keysmith/v1`。`blockers` 非空或 `ok=false` 即失败关闭。

## Codex (`third_party/keysmith/codex/codex-instruct.py`)

| 统一命令 | argv |
| --- | --- |
| version | `--version` |
| status | `--status --codex-dir <abs> --lang en` |
| plan-activate | `--file <abs.md> --name <safe> --codex-dir <abs> --dry-run --lang en` |
| activate | `--file <abs.md> --name <safe> --codex-dir <abs> --yes --lang en` |
| plan-deactivate | `--uninstall --codex-dir <abs> --lang en` |
| deactivate | `--uninstall --codex-dir <abs> --yes --lang en` |
| doctor | 与 status 相同（无独立 doctor） |
| recover | `--recover --codex-dir <abs> --lang en` 确认后加 `--yes` |
| scenario-list | `--scenario-list --lang en` |
| scenario-status | `--scenario-status [--target-dir <abs>] [--scenario-root <abs>] --lang en` |
| scenario-deploy | `--deploy-scenario <id> [--target-dir <abs>] --lang en`，确认后加 `--yes` |
| scenario-uninstall | `--scenario-uninstall <deployment id> [--target-dir <abs>] --lang en`，确认后加 `--yes` |
| scenario-recover | `--scenario-recover [--target-dir <abs>] --lang en`，确认后加 `--yes` |
| scaffold-list | `--scaffold-list [--pack-dir <abs>] --lang en` |
| scaffold | `--scaffold <pack> [--pack-dir <abs>] --lang en`，确认后加 `--yes` |
| scaffold-uninstall | `--scaffold-uninstall <pack> --lang en`，确认后加 `--yes` |

无稳定 JSON。解析结构化文本字段：`配置激活状态` / `activation`、`conflict`、`recovery`、journal、paths。scope 仅 `user`。不传 `--json`。不搬 `--preset`。内置 overlay 是 `third_party/keysmith/codex/examples/gpt-overlay.md`，跟其他示例一样可导入，不通过 CLI 选择。预览默认不加 `--yes`。

## Grok (`third_party/keysmith/grok/grok-keysmith.py`)

| 统一命令 | argv |
| --- | --- |
| version | `--version` |
| status | `--status --json --grok-dir <abs>` |
| plan-activate | `--file <abs.md> --dry-run --json --grok-dir <abs>` |
| activate | `--file <abs.md> --expected-preview-token <64 hex> --yes --json --grok-dir <abs>` |
| plan-deactivate | `--uninstall --json --grok-dir <abs>` |
| deactivate | `--uninstall --expected-preview-token <64 hex> --yes --json --grok-dir <abs>` |
| doctor | `--status --json --grok-dir <abs>` |
| recover | `--recover --json --grok-dir <abs>`。确认时加 `--expected-preview-token <64 hex> --yes` |
| reconcile | `--reconcile --json --grok-dir <abs>`。确认时加 `--expected-preview-token <64 hex> --yes` |

`--grok-dir` 必须绝对路径。schema: `grok-keysmith.envelope.v1`。状态：`not-installed` / `active-aligned` / `inactive` / `drift` / `conflict` / `recovery-required`。scope 仅 `user`。

确认 token 来自预览 envelope 的 `plan.confirmation_token`，不是 Switch 自己的 operation id。预览本身不带 `--yes`，也不带 token。

进阶 `run` 传 `--prompt` / `--mode` / `--timeout` 等，不再退回 `--help`。`breaktest` 必须带 `--bank`。两者按行发 `advanced-output`，`cancel_advanced` 结束进程。

## ZCode (`third_party/keysmith/zcode/zcode-keysmith.py`)

| 统一命令 | argv |
| --- | --- |
| version | `--version` |
| status | `doctor` |
| plan-activate | `install --system-file <abs.md> --dry-run` |
| activate | `install --system-file <abs.md> --yes` |
| plan-deactivate | `uninstall --dry-run --json` |
| deactivate | `uninstall --yes --json`。`--json` 在 `--yes` 之后 |
| doctor | `doctor` |
| recover | 不支持：envelope `ok=false`，`unavailableReason` 说明无 recover |

仅 macOS。Windows 不调用 CLI。scope 仅 `user`。不支持 recover。

doctor / install 继续解析文本行，不传 `--json`。0.3.2 的 `uninstall --help` 有 `--json`；带上它时 stdout 是 `zcode-keysmith/v1`（`operation=uninstall`，`mode=preview|execute`，`write` 与 `removed`）。plan-deactivate / deactivate 传 `--json`。解析器仍接受不带 `--json` 的文本行。`--json` 不用于 doctor、install 或 `--version`。

## pi (`third_party/keysmith/pi/pi-keysmith.py`)

| 统一命令 | argv |
| --- | --- |
| version | `--version`（argparse 文本，不是 envelope） |
| status | `--status --pi-dir <abs> --json --lang en` |
| plan-activate | `--file <abs.md> --name <safe> --pi-dir <abs> --dry-run --json --lang en` |
| activate | `--file <abs.md> --name <safe> --pi-dir <abs> --expected-preview-token <64 hex> --yes --json --lang en` |
| plan-deactivate | `--uninstall --pi-dir <abs> --json --lang en` |
| deactivate | `--uninstall --pi-dir <abs> --expected-preview-token <64 hex> --yes --json --lang en` |
| doctor | 同 status |
| recover | `--recover --pi-dir <abs> --json --lang en`。确认时加 `--expected-preview-token <64 hex> --yes` |
| backups / restore / reconcile | 不支持 |

`--pi-dir` 每次都传，且必须是绝对路径：隔离 home 时是 `<home>/.pi/agent`，否则是真实 home 下的 `~/.pi/agent`。这一点与 Grok 不同。CLI 从不创建这个目录；目录不存在时 status 为 `not-installed`，部署被 `pi-dir-missing` 拦下。schema: `pi-keysmith.envelope.v1`，契约见 pi-keysmith `v0.2.0` 的 `docs/json-contract.md`。scope 仅 `user`；`target.scope` 不是 `user`，或 `version` 低于 `0.2.0`，都按契约破坏处理。只写 `SYSTEM.md` 与它自己的 manifest，不动 `APPEND_SYSTEM.md`、`AGENTS.md`、`CLAUDE.md`、`settings.json`、`models.json`。

`normalize_pi` 与 `normalize_grok` 分开：

- 状态在 `status.*`：`not-installed` / `conflict` / `recovery-required` / `drift` / `active-aligned`（映射为 `active`）。没有 `inactive`。部署预览与确认上的 `drift` 不算需要修复：pi 会备份并替换手改过的 `SYSTEM.md`。
- status 在 `conflict` / `recovery-required` 时 `ok=false`、exit 1，但这是有效状态，不当成 CLI 故障；`drift` 的 exit 是 0。
- `diagnostics` 是 `"<code>: <说明>"`，只按第一个冒号前的 code 匹配。全部进 `warnings`；`windows-beta` 只是 warning。
- blockers：预览和确认取 `plan.blockers`，status 按操作取 `status.blockers.deploy` / `.uninstall`；code 换成对应的 diagnostic 句子。
- 确认 token 只取 `plan.confirmation_token`，必须是 64 位小写 hex。
- `plan.writes[]` 是计划文件（路径拼在 `pi_dir` 下），`status.nodes.system` 是当前规则节点（`fingerprint.sha256` → `currentFingerprint`），`status.residue` 非空时提示 recover。
- 退出码 2（用法错误）、3（`preview-token-mismatch`，提示重新预览）、5（`lock-busy`，可重试）都保证零写入；只有 4（`write-failed`）标记需要 recover。

清理只走 adapter 自己的 uninstall，不动 pi 的会话、设置和其他文件。输入替换不支持 pi。
