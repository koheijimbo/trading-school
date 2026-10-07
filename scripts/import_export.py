#!/usr/bin/env python3
"""Claude上の控えから書き出した号を data/ に取り込み、index.json を作り直す。

使い方: python3 scripts/import_export.py <書き出し先ディレクトリ>

書き出し先ディレクトリの中身（ArtifactData の out_dir 形式）:
  briefings/YYYY-MM-DD.json  →  data/briefings/YYYY-MM-DD.json
  structure/current.json     →  data/structure.json（あれば）

公開ページに出す前の整形もここで行う: 項目の順番をそろえ、非公開ページへの
リンク（deckUrl）を落とし、https 以外のURLを空にする。
検査に失敗したファイルは取り込まず、終了コード 1 で止まる。
"""
import json
import pathlib
import re
import sys

import build_index

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ORDER = ["date", "edition", "status", "updatedAt", "headline", "lede", "takeaways", "markets",
         "drivers", "news", "watch", "calendar", "analysis", "sources", "notes"]
PRIVATE_KEYS = {"deckUrl"}


def clean_urls(items):
    for item in items or []:
        if isinstance(item, dict) and "url" in item and not str(item["url"]).startswith("https://"):
            item["url"] = ""


def normalize(doc):
    out = {key: doc[key] for key in ORDER if key in doc}
    for key, value in doc.items():
        if key not in out and key not in PRIVATE_KEYS and not key.startswith("_"):
            out[key] = value
    clean_urls(out.get("news"))
    clean_urls(out.get("sources"))
    return out


def write_if_changed(path, doc):
    text = json.dumps(doc, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return "変更なし"
    existed = path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return "更新" if existed else "追加"


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 1
    src = pathlib.Path(sys.argv[1])
    files = sorted((src / "briefings").glob("*.json"))
    if not files:
        print(f"NG: {src}/briefings に号がありません", file=sys.stderr)
        return 1

    errors = []
    for path in files:
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            errors.append(f"{path.name}: JSONとして読めません ({exc})")
            continue
        date = doc.get("date") if isinstance(doc, dict) else None
        if not isinstance(date, str) or not DATE_RE.match(date) or date != path.stem:
            errors.append(f"{path.name}: date がファイル名と一致しません")
            continue
        if not isinstance(doc.get("headline"), str) or not doc["headline"].strip():
            errors.append(f"{path.name}: headline がありません")
            continue
        result = write_if_changed(ROOT / "data" / "briefings" / f"{date}.json", normalize(doc))
        print(f"{result}: {date} {doc.get('edition', '')} {doc['headline']}")

    structure = src / "structure" / "current.json"
    if structure.exists():
        try:
            doc = json.loads(structure.read_text(encoding="utf-8"))
            clean_urls(doc.get("sources"))
            print(f"{write_if_changed(ROOT / 'data' / 'structure.json', doc)}: 構造データ（{doc.get('asOf', '日付なし')}時点）")
        except (OSError, ValueError) as exc:
            errors.append(f"structure/current.json: JSONとして読めません ({exc})")

    if errors:
        for line in errors:
            print("NG:", line, file=sys.stderr)
        return 1
    return build_index.main()


if __name__ == "__main__":
    sys.exit(main())
