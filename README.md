# 政局×マーケット日報

為替・株式取引に効くニュースと、政権・議会・日銀の構造を毎日まとめる日報です。
このブランチ（`gh-pages`）の内容が GitHub Pages でそのまま公開されます。

公開URL: https://koheijimbo.github.io/trading-school/

## 構成

| パス | 内容 |
|---|---|
| `index.html` | ページ本体。下のデータを読み込んで表示する |
| `data/briefings/YYYY-MM-DD.json` | その日の号。1日1ファイル |
| `data/structure.json` | 政権・議会・日銀の構造。人事や議席が動いた日だけ直す |
| `data/index.json` | 号の一覧。手で編集せず、下のスクリプトで作り直す |
| `scripts/build_index.py` | `data/index.json` を作り直し、データの形を検査する |
| `scripts/import_export.py` | Claude 上の控えから書き出した号を `data/` に取り込む |

## 更新の流れ

1. 毎日17:47ごろ（日本時間）に、Claude のスケジュールタスクがその日の号を作り、Claude 上の非公開の控えに保存する。ここではまだ公開されない
2. 内容を確認し、Claude のチャットで「日報を公開して」と伝える
3. Claude が控えを書き出し、`python3 scripts/import_export.py <書き出し先>` で `data/` に取り込み、このブランチにコミットしてプッシュする
4. 1〜2分で公開URLに反映される

`scripts/import_export.py` は取り込みのあと `scripts/build_index.py` も実行する。
号のファイルを手で直した場合は `python3 scripts/build_index.py` を実行してからコミットする。

## 注意

本ページは情報提供を目的としたものであり、特定の金融商品の売買を推奨するものではありません。
