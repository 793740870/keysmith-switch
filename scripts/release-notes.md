# Keysmith Switch v0.6.5

输入替换支持**密封规则包**：拓展仓库可以发布 `opaque: true` 的规则包，App 只展示名称、条数和适用的 Agent，不展示规则正文。

## 这一版有什么

- **密封规则包。** 安装时只显示名称、条数和适用的 Agent，按钮是「安装」而不是「查看规则」。在「输入替换」页，这张表只显示条数和「密封」说明，没有规则列表，也没有「复制到我的规则」。
  - 已启用的密封表有新版本时，仍要你确认才会切换；确认框只展示版本号和新旧条数，不展示差异。
  - 中转服务照常按原文替换，替换效果和普通规则包一样。
  - 密封只是界面上不展示，不是加密：规则在本机数据库、备份和 `~/.keysmith-switch/input-rewrite/rules.json` 里仍是明文。
- 普通规则包、提示词包和其他功能不受影响。目前官方源里还没有密封规则包。
- 更早的版本会把密封规则包显示为「需要新版 App」，不能安装。

## 安装

- 已安装 `v0.1.3` 及以上的版本，可以在应用内点「检查更新」升级到 `v0.6.5`，安装仍需你确认。
- macOS Apple Silicon：`Keysmith.Switch_0.6.5_aarch64.dmg`
- Windows x64：`Keysmith.Switch_0.6.5_x64-setup.exe`

安装包没有使用 Apple Developer ID、公证或 Windows Authenticode。更新包用独立的生产 minisign 密钥签名，这不是平台代码签名。

Windows 上如果火绒等杀毒软件提示有病毒：只要是从本页下载的，就是误报，可以放心使用。在杀毒软件的「隔离区」恢复被隔离的文件，再把 Keysmith Switch 加入「信任区」即可，详见 [README](https://github.com/Jia-Ethan/keysmith-switch#-下载)。
