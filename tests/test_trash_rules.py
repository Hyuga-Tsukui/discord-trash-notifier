from datetime import date

from src.trash_rules import get_trash_info


def test_weekday_rules():
    assert get_trash_info(date(2026, 2, 2)).types == ["プラスチック製容器包装"]  # Monday
    assert get_trash_info(date(2026, 2, 3)).types == ["普通ごみ"]  # Tuesday
    assert get_trash_info(date(2026, 2, 4)).types == ["ミックスペーパー"]  # Wednesday
    assert get_trash_info(date(2026, 2, 6)).types == ["普通ごみ"]  # Friday


def test_thursday_rules():
    assert get_trash_info(date(2026, 2, 5)).types == [
        "空き缶",
        "ペットボトル",
        "空きびん",
        "使用済み乾電池",
    ]  # 1st Thu

    assert get_trash_info(date(2026, 2, 12)).types == [
        "空き缶",
        "ペットボトル",
        "空きびん",
        "使用済み乾電池",
        "小物金属",
    ]  # 2nd Thu

    assert get_trash_info(date(2026, 2, 26)).types == [
        "空き缶",
        "ペットボトル",
        "空きびん",
        "使用済み乾電池",
        "小物金属",
    ]  # 4th Thu


def test_weekend_no_notification():
    assert get_trash_info(date(2026, 2, 7)) is None  # Saturday
    assert get_trash_info(date(2026, 2, 8)) is None  # Sunday
