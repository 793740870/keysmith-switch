# Keysmith Switch v0.8.1

新增第六个 Agent：**DSH（DeepSeek Harness）**。可以把提示词库里的提示词部署到 DSH：先看部署计划，确认后再写入。

## 这一版有什么

- **DSH。** 侧栏多了 DSH 的入口，使用自带的 dsh-keysmith 0.2.2，不需要另外安装。
  - 只写全局的 `~/.dsh/AGENTS.md` 和 `~/.dsh/cordis.patch.yml`；`settings.yaml`、`.credentials.yaml`、会话和存储都不会改。
  - 原来已有、或被手动改过的 `AGENTS.md` 会先备份再替换；停用时放回原来的内容。
  - `~/.dsh` 不存在时不会替你创建，部署会被拦下并说明原因。
  - 部署或停用中途被打断时，可以预览并执行恢复。
  - DSH 适配器的流式 tool-call 热修会在源码匹配时应用；上游改动后会跳过并在计划里明确说明。
  - 输入替换暂不支持 DSH。
- 其他 Agent 和功能不受影响。

## 安装

- 已安装 `v0.1.3` 及以上的版本，可以在应用内点「检查更新」升级到 `v0.8.1`，安装仍需你确认。
- macOS Apple Silicon：`Keysmith.Switch_0.8.1_aarch64.dmg`
- Windows x64：`Keysmith.Switch_0.8.1_x64-setup.exe`

安装包没有使用 Apple Developer ID、公证或 Windows Authenticode。更新包用独立的生产 minisign 密钥签名，这不是平台代码签名。

Windows 上如果火绒等杀毒软件提示有病毒：只要是从本页下载的，就是误报，可以放心使用。在杀毒软件的「隔离区」恢复被隔离的文件，再把 Keysmith Switch 加入「信任区」即可，详见 [README](https://github.com/Jia-Ethan/keysmith-switch#-下载)。
