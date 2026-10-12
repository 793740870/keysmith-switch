# Keysmith Switch v0.7.0

新增第五个 Agent：**pi**。和 Claude Code、Codex、Grok Build、ZCode 一样，可以把提示词库里的提示词部署到 pi：先看部署计划，确认后再写入。

## 这一版有什么

- **pi。** 侧栏多了 pi 的入口，使用自带的 pi-keysmith 0.2.0，不需要另外安装。
  - 只写全局的 `~/.pi/agent/SYSTEM.md` 和 pi-keysmith 自己的记录文件；`APPEND_SYSTEM.md`、`AGENTS.md`、`CLAUDE.md`、`settings.json`、`models.json` 都不会改。
  - 原来已有、或被手动改过的 `SYSTEM.md` 会先备份再替换；停用时放回原来的内容。
  - `~/.pi/agent` 不存在（还没用过 pi）时不会替你创建，部署会被拦下并说明原因。
  - 部署或停用中途被打断时，可以在 App 里预览并执行恢复。
  - 「清理」只停用 pi 的部署，不动它的会话、设置和其他文件。
  - 输入替换暂不支持 pi。
- 其他 Agent 和功能不受影响。

## 安装

- 已安装 `v0.1.3` 及以上的版本，可以在应用内点「检查更新」升级到 `v0.7.0`，安装仍需你确认。
- macOS Apple Silicon：`Keysmith.Switch_0.7.0_aarch64.dmg`
- Windows x64：`Keysmith.Switch_0.7.0_x64-setup.exe`

安装包没有使用 Apple Developer ID、公证或 Windows Authenticode。更新包用独立的生产 minisign 密钥签名，这不是平台代码签名。

Windows 上如果火绒等杀毒软件提示有病毒：只要是从本页下载的，就是误报，可以放心使用。在杀毒软件的「隔离区」恢复被隔离的文件，再把 Keysmith Switch 加入「信任区」即可，详见 [README](https://github.com/Jia-Ethan/keysmith-switch#-下载)。
