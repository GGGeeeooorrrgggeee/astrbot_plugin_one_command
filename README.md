# 一个指令

<p align="center">
  <img src="https://count.getloli.com/@astrbot_plugin_one_command?name=astrbot_plugin_one_command&theme=random&padding=7&offset=0&align=top&scale=1&pixelated=1&darkmode=auto" alt="Moe Counter">
</p>

<p align="center" style="margin-top: 8px; font-size: 18px;">
  ✨<a href="https://github.com/AstrBotDevs/AstrBot" target="_blank">AstrBot</a> 可配置单指令文本/图片回复插件✨
</p>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/Platform-aiocqhttp-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/Version-1.0.0-orange" alt="Version">
  <a href="https://github.com/GGGeeeooorrrgggeee/astrbot_plugin_one_command"><img src="https://img.shields.io/github/stars/GGGeeeooorrrgggeee/astrbot_plugin_one_command" alt="Stars"></a>
  <a href="https://github.com/GGGeeeooorrrgggeee/astrbot_plugin_one_command/commits/main"><img src="https://img.shields.io/github/last-commit/GGGeeeooorrrgggeee/astrbot_plugin_one_command" alt="Last Commit"></a>
</p>


<p align="center">
  <strong>Language / 语言</strong><br>
  <a href="README.md"><img src="https://img.shields.io/badge/中文-当前-blue" alt="中文"></a>
</p>

---

## 一、简介

`一个指令` 是一个面向 [AstrBot](https://github.com/AstrBotDevs/AstrBot) 的轻量插件。

插件提供一个可在配置中修改名称和前缀的唯一指令。用户触发该指令后，插件可以按配置发送文本、图片，或者文本加图片。

插件不依赖 AstrBot 全局指令前缀，而是使用插件自己的指令前缀配置。默认触发格式为 `/一个指令`；如果将插件指令前缀留空，则可以使用裸指令 `一个指令` 触发。

## 二、项目信息

- 作者：[George](https://github.com/GGGeeeooorrrgggeee)
- 版本：1.0.0
- 插件名：`astrbot_plugin_one_command`
- 仓库：[astrbot_plugin_one_command](https://github.com/GGGeeeooorrrgggeee/astrbot_plugin_one_command)
- 支持平台：`aiocqhttp`

## 三、核心功能

| 功能 | 说明 |
|:---|:---|
| 自定义指令名称 | 可在 AstrBot 插件配置中修改唯一触发指令的名称 |
| 自定义指令前缀 | 使用插件自己的前缀配置，不跟随 AstrBot 全局指令前缀 |
| 裸指令触发 | 指令前缀配置为空时，可直接发送指令名称触发 |
| 文本回复 | 发送配置中的文本内容；文本为空时返回 `文本信息为空喵~` |
| 图片回复 | 通过 `file` 配置上传图片并发送；图片为空、无效或多张时返回对应提示 |
| 文本+图片回复 | 文本和图片会合并在同一条消息中发送，中间始终换行 |
| 单图片限制 | 只允许上传一张图片；如果配置多张图片，图片发送失效 |
| 合并转发 | 可选择使用 QQ 合并转发格式发送消息 |

## 四、文件结构

```text
astrbot_plugin_one_command/
├── main.py              # 插件入口与消息处理
├── _conf_schema.json    # AstrBot 插件配置项
├── metadata.yaml        # 插件元数据
├── README.md            # 项目说明文档
└── logo.png             # 插件图标
```

## 五、依赖

```text
无额外第三方依赖
```

插件仅使用 AstrBot 提供的插件 API 和 Python 标准库。

## 六、安装

1. 通过 AstrBot 插件管理使用 zip 压缩包或仓库链接安装。
2. 在插件配置中按需修改指令前缀、指令名称、发送类型、文本、图片和合并转发开关。
3. 重载或重启 AstrBot。

## 七、配置说明

| 配置项 | 类型 | 默认值 | 说明 |
|:---|:---|:---|:---|
| `command_name` | `string` | `一个指令` | 唯一触发指令的名称，不需要填写前缀 |
| `command_prefix` | `string` | `/` | 插件自己的指令前缀，不跟随 AstrBot 全局指令前缀；留空则使用裸指令 |
| `send_type` | `string` | `文本` | 触发后发送的内容类型，可选 `文本`、`图片`、`文本+图片` |
| `text` | `text` | `这是一个文本信息。` | 文本模式或文本+图片模式要发送的文本信息 |
| `image` | `file` | 空 | 要发送的图片文件，仅限 `bmp`、`gif`、`jpeg`、`jpg`、`png`、`webp` |
| `merge_send` | `bool` | `false` | 是否使用 QQ 合并转发格式发送 |

### 图片配置

图片通过 AstrBot 的 `file` 类型配置上传。上传后的文件通常位于 AstrBot 数据目录下，例如：

```text
AstrBot/data/plugin_data/astrbot_plugin_one_command/files
```

插件会根据配置值自动解析图片路径。图片为空或不是有效图片时，会返回 `图片信息为空喵~`；上传超过一张图片时，会返回 `图片文件仅能上传一张喵~`。在 `文本+图片` 模式下，图片或图片提示会和文本放在同一条消息里发送，并且中间换行。

当前允许上传的图片后缀为：

```text
bmp, gif, jpeg, jpg, png, webp
```

## 八、指令说明

插件指令不跟随 AstrBot 全局指令前缀，只使用本插件配置中的 `command_prefix`。

插件会优先读取平台原始消息内容进行匹配，因此即使 AstrBot 全局指令前缀和本插件的 `command_prefix` 相同，也仍然按本插件配置判断触发。

| 配置示例 | 触发方式 | 说明 |
|:---|:---|:---|
| `command_prefix=/`，`command_name=一个指令` | `/一个指令` | 默认触发方式 |
| `command_prefix=!`，`command_name=一个指令` | `!一个指令` | 自定义前缀 |
| `command_prefix=`，`command_name=一个指令` | `一个指令` | 前缀留空时使用裸指令 |

## 九、发送类型说明

| 发送类型 | 行为 |
|:---|:---|
| `文本` | 只发送配置中的文本，不检查图片配置 |
| `图片` | 只发送配置中的图片；图片为空或非图片时返回 `图片信息为空喵~`，多于一张时返回 `图片文件仅能上传一张喵~` |
| `文本+图片` | 在同一条消息里发送文本和图片；文本和图片中间始终换行 |

如果 `文本+图片` 模式下文本和图片都为空，会在同一条消息中返回：

```text
文本信息为空喵~
图片信息为空喵~
```

## 十、合并转发说明

开启 `merge_send` 后，插件会尝试使用 QQ 合并转发节点发送消息。

该功能依赖 OneBot/QQ 平台能力，插件元数据目前限定支持 `aiocqhttp`。如果机器人 ID 无法构造合并转发节点，插件会回退为普通消息发送。

## 十一、注意事项

1. `command_name` 不需要填写前缀，前缀请填写到 `command_prefix`。
2. `command_prefix` 为空时才会使用裸指令；默认 `/` 不会触发裸指令。
3. 插件使用原始消息匹配，避免被 AstrBot 全局指令前缀剥离影响。
4. 文本为空时会返回 `文本信息为空喵~`，图片为空或无效时会返回 `图片信息为空喵~`。
5. 图片配置只能上传一张图片，多于一张时会返回 `图片文件仅能上传一张喵~`。
6. 图片文件后缀必须是 `bmp`、`gif`、`jpeg`、`jpg`、`png` 或 `webp`。
7. 合并转发主要面向 QQ/OneBot 场景，其他平台不保证支持。
