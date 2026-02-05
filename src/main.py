from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from .config import load_config
from .discord_client import DiscordClient
from .trash_rules import get_trash_info


def build_message(trash_types: list[str]) -> str:
    joined = " / ".join(trash_types)
    return f"今日のゴミ出し: {joined}"


def main() -> int:
    jst = ZoneInfo("Asia/Tokyo")
    today_jst = datetime.now(tz=jst).date()

    trash_info = get_trash_info(today_jst)
    if trash_info is None:
        return 0

    config = load_config()
    client = DiscordClient(config.discord_bot_token, config.discord_channel_id)
    client.send_message(build_message(trash_info.types))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
