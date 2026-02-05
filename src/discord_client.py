from __future__ import annotations

import requests


class DiscordClient:
    def __init__(self, bot_token: str, channel_id: str) -> None:
        self._bot_token = bot_token
        self._channel_id = channel_id

    def send_message(self, content: str) -> None:
        url = f"https://discord.com/api/v10/channels/{self._channel_id}/messages"
        headers = {
            "Authorization": f"Bot {self._bot_token}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, json={"content": content}, headers=headers, timeout=10)
        if not response.ok:
            raise RuntimeError(
                f"Discord API error: status={response.status_code} body={response.text}"
            )
