from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    discord_bot_token: str
    discord_channel_id: str


def load_config() -> Config:
    load_dotenv()

    token = os.getenv("DISCORD_BOT_TOKEN")
    channel_id = os.getenv("DISCORD_CHANNEL_ID")

    missing = [
        name
        for name, value in (
            ("DISCORD_BOT_TOKEN", token),
            ("DISCORD_CHANNEL_ID", channel_id),
        )
        if not value
    ]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    return Config(discord_bot_token=token, discord_channel_id=channel_id)
