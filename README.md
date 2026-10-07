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

## 更新の流れ

毎日17:47ごろ（日本時間）に、Claude のスケジュールタスクが次の順で更新します。

1. その日のニュースを調べ、`data/briefings/YYYY-MM-DD.json` を書く
2. 人事・議席・政策金利が変わった日は `data/structure.json` も直す
3. `python3 scripts/build_index.py` を実行する
4. このブランチにコミットしてプッシュする

手で直す場合も、号のファイルを編集したあとに手順3と4を行ってください。

## 注意

本ページは情報提供を目的としたものであり、特定の金融商品の売買を推奨するものではありません。
