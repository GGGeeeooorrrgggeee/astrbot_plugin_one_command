from __future__ import annotations

from pathlib import Path
from urllib.parse import unquote, urlparse

from astrbot.api import AstrBotConfig, logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.message_components import Image, Node, Plain
from astrbot.api.star import Context, Star, register


PLUGIN_NAME = "astrbot_plugin_one_command"
DEFAULT_COMMAND = "一个指令"
DEFAULT_PREFIX = "/"
DEFAULT_TEXT = "这是一个文本信息。"
EMPTY_TEXT_NOTICE = "文本信息为空喵~"
EMPTY_IMAGE_NOTICE = "图片信息为空喵~"
TOO_MANY_IMAGES_NOTICE = "图片文件仅能上传一张喵~"
IMAGE_EXTENSIONS = {".bmp", ".gif", ".jpeg", ".jpg", ".png", ".webp"}
SEND_TYPES = {"文本", "图片", "文本+图片"}


@register(
    PLUGIN_NAME,
    "George",
    "可配置一个指令，并发送文本、图片或文本加图片。",
    "1.0.0",
    "https://github.com/GGGeeeooorrrgggeee/astrbot_plugin_one_command",
)
class OneCommandPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig | None = None):
        super().__init__(context)
        self.config = config or {}

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent):
        """匹配配置中的唯一指令并发送配置的内容。"""
        command_name = self._command_name()
        command_prefix = self._command_prefix()
        message_text = self._original_message_text(event)
        if not self._is_triggered(message_text, command_prefix, command_name):
            return

        # 命令已经匹配，即使图片配置无效也要消费掉这条消息，避免继续触发其他处理。
        event.stop_event()

        send_type = self._send_type()
        text = self._text()
        image_result = (
            self._image_result()
            if send_type in {"图片", "文本+图片"}
            else (None, EMPTY_IMAGE_NOTICE)
        )
        image_source, image_notice = image_result

        if send_type == "文本":
            yield self._result(event, [Plain(text or EMPTY_TEXT_NOTICE)], "文本")
            return

        if send_type == "图片":
            if image_source is None:
                logger.warning(
                    "%s：图片模式未发送图片，图片配置必须且只能包含一个有效图片文件。",
                    PLUGIN_NAME,
                )
                yield self._result(event, [Plain(image_notice)], "图片")
                return
            yield self._result(
                event,
                [self._image_component(image_source)],
                "图片",
            )
            return

        chain = [Plain(f"{text or EMPTY_TEXT_NOTICE}\n")]
        if image_source is not None:
            chain.append(self._image_component(image_source))
        else:
            chain.append(Plain(image_notice))
        yield self._result(event, chain, "文本+图片")

    def _result(self, event: AstrMessageEvent, chain: list, mode: str):
        """根据合并转发开关生成普通消息链或 QQ 转发节点。"""
        if not self._merge_send():
            return event.chain_result(chain)

        bot_id = str(getattr(event.message_obj, "self_id", "") or "")
        if not bot_id.isdigit():
            logger.warning(
                "%s：当前平台的机器人 ID 不是数字，无法构造 QQ 合并转发，改用普通消息发送。",
                PLUGIN_NAME,
            )
            return event.chain_result(chain)

        try:
            node = Node(
                uin=int(bot_id),
                name=self._forward_name(event, mode),
                content=chain,
            )
            return event.chain_result([node])
        except Exception as exc:
            logger.warning(
                "%s：构造合并转发失败，改用普通消息发送：%s",
                PLUGIN_NAME,
                exc,
            )
            return event.chain_result(chain)

    def _command_name(self) -> str:
        value = self._config_value("command_name", DEFAULT_COMMAND)
        command = str(value).strip()
        return command.lstrip("/") or DEFAULT_COMMAND

    def _command_prefix(self) -> str:
        value = self._config_value("command_prefix", DEFAULT_PREFIX)
        return str(value).strip()

    def _send_type(self) -> str:
        value = str(self._config_value("send_type", "文本")).strip()
        return value if value in SEND_TYPES else "文本"

    def _text(self) -> str:
        value = self._config_value("text", DEFAULT_TEXT)
        return str(value).strip() if value is not None else DEFAULT_TEXT

    def _merge_send(self) -> bool:
        return bool(self._config_value("merge_send", False))

    def _config_value(self, key: str, default):
        try:
            value = self.config.get(key, default)
        except AttributeError:
            return default
        return default if value is None else value

    @staticmethod
    def _original_message_text(event: AstrMessageEvent) -> str | None:
        message_obj = getattr(event, "message_obj", None)
        message_text = getattr(message_obj, "message_str", None)
        if message_text is not None:
            return str(message_text)
        return event.message_str

    @staticmethod
    def _is_triggered(
        message: str | None,
        command_prefix: str,
        command_name: str,
    ) -> bool:
        if not message:
            return False
        content = message.strip()
        return content == f"{command_prefix}{command_name}"

    def _image_result(self) -> tuple[str | None, str]:
        candidates = self._image_candidates()
        if len(candidates) != 1:
            if candidates:
                logger.warning(
                    "%s：图片配置包含 %d 个文件，要求恰好上传一张，当前不发送图片。",
                    PLUGIN_NAME,
                    len(candidates),
                )
                return None, TOO_MANY_IMAGES_NOTICE
            return None, EMPTY_IMAGE_NOTICE

        candidate = candidates[0]
        source = self._resolve_image_source(candidate)
        if source is None:
            logger.warning(
                "%s：图片配置不是有效的图片文件（配置值：%s），当前不发送图片。",
                PLUGIN_NAME,
                candidate,
            )
            return None, EMPTY_IMAGE_NOTICE
        return source, ""

    def _image_candidates(self) -> list[str]:
        value = self._config_value("image", [])
        if isinstance(value, (list, tuple)):
            raw_items = list(value)
        elif value:
            raw_items = [value]
        else:
            raw_items = []

        candidates: list[str] = []
        for item in raw_items:
            if isinstance(item, dict):
                item = item.get("path") or item.get("file") or item.get("url")
            if item is not None and str(item).strip():
                candidates.append(str(item).strip())
        return candidates

    @staticmethod
    def _to_local_path(value: str) -> Path | None:
        if value.startswith("file://"):
            parsed = urlparse(value)
            raw_path = unquote(parsed.path)
            if parsed.netloc:
                raw_path = f"//{parsed.netloc}{raw_path}"
            if len(raw_path) >= 3 and raw_path[0] == "/" and raw_path[2] == ":":
                raw_path = raw_path[1:]
            value = raw_path
        return Path(value)

    @classmethod
    def _resolve_image_source(cls, value: str) -> str | None:
        """解析 file 配置返回的绝对路径、相对路径、data 路径或图片 URL。"""
        if value.startswith(("http://", "https://")):
            suffix = Path(urlparse(value).path).suffix.lower()
            return value if suffix in IMAGE_EXTENSIONS else None

        path = cls._to_local_path(value)
        if path is None:
            return None

        roots = [
            Path.cwd(),
            Path(__file__).resolve().parent,
        ]
        plugin_dir = Path(__file__).resolve().parent
        if len(plugin_dir.parents) >= 3:
            roots.append(plugin_dir.parents[2])
        if len(plugin_dir.parents) >= 4:
            roots.append(plugin_dir.parents[3] / "data")

        candidates: list[Path] = []
        if path.is_absolute():
            candidates.append(path)
        else:
            candidates.extend(root / path for root in roots)
            if path.parts and path.parts[0].lower() != "data":
                candidates.extend(root / "data" / path for root in roots)

        for candidate in candidates:
            if candidate.is_file() and candidate.suffix.lower() in IMAGE_EXTENSIONS:
                return str(candidate)

        # 部分版本只在配置中保存上传文件名，实际文件位于 data/plugin_data 下。
        file_name = path.name
        for root in roots:
            data_root = root if root.name.lower() == "data" else root / "data"
            if not data_root.is_dir():
                continue
            try:
                for candidate in data_root.rglob(file_name):
                    if (
                        candidate.is_file()
                        and candidate.suffix.lower() in IMAGE_EXTENSIONS
                    ):
                        return str(candidate)
            except OSError:
                continue
        return None

    @staticmethod
    def _image_component(source: str):
        if source.startswith(("http://", "https://")):
            return Image.fromURL(source)
        return Image.fromFileSystem(source)

    @staticmethod
    def _forward_name(event: AstrMessageEvent, mode: str) -> str:
        sender_name = event.get_sender_name()
        return sender_name or f"一个指令（{mode}）"

    async def terminate(self):
        """插件卸载时无需额外清理。"""
