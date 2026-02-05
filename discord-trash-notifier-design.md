---
title: Discord ゴミ出し通知（GitHub Actions + Python + uv）設計書
version: "1.1"
created: 2026-02-05
timezone: Asia/Tokyo
---

# 1. ゴール

Discord の指定チャンネルに、毎日「当日のゴミ出し種別」を通知する。実行は GitHub Actions の `schedule`（cron）で行い、Python スクリプトが日付ロジックを判定して Discord API へ投稿する。

---

# 2. 全体構成

## 2.1 アーキテクチャ

```text
GitHub Actions (cron, UTC)
  └─ Python runner
      ├─ JSTで「今日」を算出
      ├─ ゴミ種別を判定（曜日 + 第2/第4木曜）
      └─ Discord API にメッセージ投稿
```

---

# 3. 採用技術

- スケジューラ: GitHub Actions
- 実装言語: Python
- 通知: Discord API（Botトークン）
- Python環境管理: **uv**

---

# 4. 開発環境セットアップ（uv 必須）

## 4.1 uv 採用理由

- 依存解決が高速
- 仮想環境を統合管理可能
- `pip` + `venv` を置き換えるモダンツール
- GitHub Actions との相性が良い

---

## 4.3 プロジェクト初期化

```bash
uv init discord-trash-notifier
cd discord-trash-notifier
```

---

## 4.4 依存パッケージ追加

```bash
uv add requests python-dotenv
```

---

## 4.5 仮想環境起動

```bash
uv sync
```

---

# 5. プロジェクト構成

```text
discord-trash-notifier/
  pyproject.toml
  uv.lock
  src/
    main.py
    trash_rules.py
    discord_client.py
    config.py
  .github/
    workflows/
      notify.yml
```

---

# 6. 実装ルール（AI向け）

## 6.1 Python仕様

- Python 3.11以上
- タイムゾーンは `zoneinfo.ZoneInfo("Asia/Tokyo")`
- ロジックと I/O を分離

### 責務分離

| ファイル          | 役割               |
| ----------------- | ------------------ |
| trash_rules.py    | 日付 → ゴミ種別    |
| discord_client.py | Discord送信        |
| config.py         | 環境変数読み込み   |
| main.py           | エントリーポイント |

---

# 7. ゴミ出しルール

## 曜日ルール

- 月曜: プラスチック製容器包装
- 火曜: 普通ごみ
- 水曜: ミックスペーパー
- 木曜: 空き缶 / ペットボトル / 空きびん / 使用済み乾電池
- 金曜: 普通ごみ
- 土日: 通知なし

## 追加ルール

### 第2・第4木曜

「小物金属」を追加

---

# 8. Discord 投稿仕様

## 必須環境変数

```
DISCORD_BOT_TOKEN
DISCORD_CHANNEL_ID
```

---

## 投稿方法

HTTP POST

```
POST https://discord.com/api/v10/channels/{channel_id}/messages
```

Header:

```
Authorization: Bot <TOKEN>
Content-Type: application/json
```

Body:

```
{
  "content": "通知メッセージ"
}
```

---

# 9. GitHub Actions 仕様

## 9.1 cron

GitHub Actions は **UTC基準**

例:

| JST   | UTC           |
| ----- | ------------- |
| 07:00 | 22:00（前日） |

---

## 9.2 workflow 例

```yaml
name: Notify Trash

on:
  schedule:
    - cron: "0 22 * * *"
  workflow_dispatch:

jobs:
  notify:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Sync dependencies
        run: uv sync

      - name: Run script
        env:
          DISCORD_BOT_TOKEN: ${{ secrets.DISCORD_BOT_TOKEN }}
          DISCORD_CHANNEL_ID: ${{ secrets.DISCORD_CHANNEL_ID }}
        run: uv run python -m src.main
```

---

# 10. 非機能要件

- Secrets は GitHub Secrets で管理
- 例外発生時は非0終了
- 祝日対応は将来拡張可能

---

# 11. 参考資料

- https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions
- https://discord.com/developers/docs/resources/channel#create-message
- https://docs.astral.sh/uv/
