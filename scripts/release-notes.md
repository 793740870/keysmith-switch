# Keysmith Switch v0.6.4

Grok Build 适配器更新到 [grok-keysmith v0.8.0](https://github.com/Jia-Ethan/grok-keysmith/releases/tag/v0.8.0)：`~/.grok/config.toml` 新增「用户区域」，部署后自己加的长期配置放进去，停用时会保留。

## 这一版有什么

- **Grok Build 的配置里可以留一块自己的区域。** 在 `~/.grok/config.toml` 末尾的 `# === keysmith user region begin ===` 和 `# === keysmith user region end ===` 之间，放部署后自己加的配置，例如订阅额度用完时用 `/model` 手动切过去的 API key 备用模型。这一段不算配置被改动，部署、停用、整理和恢复时都会原样保留。以前这些配置会让 Grok 显示配置被改动、无法重新部署，停用时还会被一起抹掉。
  - 区域里不能放 `[compat.*]` 表，要以表头（`[...]`）开头。具体规则见 [grok-keysmith 使用说明](https://github.com/Jia-Ethan/grok-keysmith/blob/main/docs/reference.md)。
  - 连接输入替换后，Switch 写入的区域仍然排在文件最后，和用户区域互不影响。
- 不使用这块区域的用户不受影响。

## 安装

- 已安装 `v0.1.3` 及以上的版本，可以在应用内点「检查更新」升级到 `v0.6.4`，安装仍需你确认。
- macOS Apple Silicon：`Keysmith.Switch_0.6.4_aarch64.dmg`
- Windows x64：`Keysmith.Switch_0.6.4_x64-setup.exe`

安装包没有使用 Apple Developer ID、公证或 Windows Authenticode。更新包用独立的生产 minisign 密钥签名，这不是平台代码签名。

Windows 上如果火绒等杀毒软件提示有病毒：只要是从本页下载的，就是误报，可以放心使用。在杀毒软件的「隔离区」恢复被隔离的文件，再把 Keysmith Switch 加入「信任区」即可，详见 [README](https://github.com/Jia-Ethan/keysmith-switch#-下载)。
