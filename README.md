# Discord ゴミ出し通知（GitHub Actions + Python + uv）

Discord の指定チャンネルに、毎日「当日のゴミ出し種別」を通知するツールです。GitHub Actions の `schedule`（cron）で実行されます。

## できること

- JST 기준で「今日」を判定してゴミ出し種別を決定
- 第2・第4木曜は「小物金属」を追加
- Discord チャンネルに通知を投稿

## 必要環境

- Python 3.11 以上
- [uv](https://docs.astral.sh/uv/)
- Discord Bot（Bot Token / チャンネルID）

## セットアップ

### 1. リポジトリを取得

```bash
git clone <your-repo-url>
cd discord-trash-notifier
```

### 2. 依存関係のインストール

```bash
uv sync --dev
```

### 3. 環境変数の設定

以下の環境変数が必要です。

- `DISCORD_BOT_TOKEN`
- `DISCORD_CHANNEL_ID`

ローカル実行時は `.env` を作成して設定できます（任意）。

```env
DISCORD_BOT_TOKEN=xxxxx
DISCORD_CHANNEL_ID=xxxxx
```

### 4. ローカル実行

```bash
uv run python -m src.main
```

## GitHub Actions での運用

`.github/workflows/notify.yml` が用意されています。以下の Secrets を GitHub に登録してください。

- `DISCORD_BOT_TOKEN`
- `DISCORD_CHANNEL_ID`

cron は UTC 基準で `0 22 * * *` に設定済みです（JST 7:00 相当）。

## テスト

```bash
uv run pytest
```

## ゴミ出しルール

- 月曜: プラスチック製容器包装
- 火曜: 普通ごみ
- 水曜: ミックスペーパー
- 木曜: 空き缶 / ペットボトル / 空きびん / 使用済み乾電池
- 金曜: 普通ごみ
- 土日: 通知なし

追加ルール:

- 第2・第4木曜に「小物金属」を追加

## 主要ファイル

- `src/trash_rules.py` 日付 → ゴミ種別
- `src/discord_client.py` Discord 送信
- `src/config.py` 環境変数読み込み
- `src/main.py` エントリーポイント

## ライセンス

必要に応じて追記してください。
