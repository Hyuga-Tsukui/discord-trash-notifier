import os

import time_machine

from src import main as main_module


@time_machine.travel("2026-02-05 07:00:00+09:00")
def test_main_sends_message_on_weekday(monkeypatch):
    os.environ["DISCORD_BOT_TOKEN"] = "token"
    os.environ["DISCORD_CHANNEL_ID"] = "channel"

    sent = {}

    def fake_send_message(self, content: str) -> None:
        sent["content"] = content

    monkeypatch.setattr(main_module.DiscordClient, "send_message", fake_send_message)

    assert main_module.main() == 0
    assert (
        sent["content"]
        == "@everyone 今日のゴミ出し: 空き缶 / ペットボトル / 空きびん / 使用済み乾電池"
    )


@time_machine.travel("2026-02-07 07:00:00+09:00")
def test_main_no_send_on_weekend(monkeypatch):
    def fake_send_message(self, content: str) -> None:
        raise AssertionError("Should not send on weekend")

    monkeypatch.setattr(main_module.DiscordClient, "send_message", fake_send_message)

    assert main_module.main() == 0
