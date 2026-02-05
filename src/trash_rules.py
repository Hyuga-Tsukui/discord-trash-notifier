from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class TrashInfo:
    types: list[str]


def _is_second_or_fourth_thursday(d: date) -> bool:
    if d.weekday() != 3:
        return False
    week_index = (d.day - 1) // 7 + 1
    return week_index in (2, 4)


def get_trash_info(d: date) -> TrashInfo | None:
    weekday = d.weekday()  # Monday=0 ... Sunday=6

    if weekday == 0:
        types = ["プラスチック製容器包装"]
    elif weekday == 1:
        types = ["普通ごみ"]
    elif weekday == 2:
        types = ["ミックスペーパー"]
    elif weekday == 3:
        types = ["空き缶", "ペットボトル", "空きびん", "使用済み乾電池"]
        if _is_second_or_fourth_thursday(d):
            types.append("小物金属")
    elif weekday == 4:
        types = ["普通ごみ"]
    else:
        return None

    return TrashInfo(types=types)
