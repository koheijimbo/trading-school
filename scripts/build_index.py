#!/usr/bin/env python3
"""data/briefings/*.json から data/index.json を作り直す。号を追加・修正したら必ず実行する。

使い方: python3 scripts/build_index.py
検査に失敗した場合は index.json を書き換えず、終了コード 1 で止まる。
"""
import datetime
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BRIEFINGS = ROOT / "data" / "briefings"
STRUCTURE = ROOT / "data" / "structure.json"
INDEX = ROOT / "data" / "index.json"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LOWER_HOUSE_SEATS = 465


def main() -> int:
    errors = []
    entries = []
    for path in sorted(BRIEFINGS.glob("*.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            errors.append(f"{path.name}: JSONとして読めません ({exc})")
            continue
        date = doc.get("date") if isinstance(doc, dict) else None
        if not isinstance(date, str) or not DATE_RE.match(date):
            errors.append(f"{path.name}: date がありません")
            continue
        if path.stem != date:
            errors.append(f"{path.name}: ファイル名と date ({date}) が一致しません")
            continue
        if not isinstance(doc.get("headline"), str) or not doc["headline"].strip():
            errors.append(f"{path.name}: headline がありません")
            continue
        status = doc.get("status") if doc.get("status") in ("final", "provisional") else "final"
        nums = {}
        for market in doc.get("markets") or []:
            if not isinstance(market, dict) or market.get("carried"):
                continue
            num = market.get("num")
            if isinstance(market.get("id"), str) and isinstance(num, (int, float)) and not isinstance(num, bool):
                nums[market["id"]] = num
        entries.append({
            "date": date,
            "status": status,
            "edition": doc.get("edition") or "",
            "headline": doc["headline"],
            "nums": nums,
        })

    try:
        structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
        for house in structure.get("houses") or []:
            total = sum(p.get("seats", 0) for p in house.get("parties") or [])
            if house.get("id") == "lower" and total != LOWER_HOUSE_SEATS:
                errors.append(f"structure.json: 衆議院の議席合計が {total} です（定数 {LOWER_HOUSE_SEATS}）")
    except (OSError, ValueError) as exc:
        errors.append(f"structure.json: JSONとして読めません ({exc})")

    if errors:
        for line in errors:
            print("NG:", line, file=sys.stderr)
        return 1

    entries.sort(key=lambda e: e["date"], reverse=True)
    generated = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(timespec="seconds")
    INDEX.write_text(
        json.dumps({"generatedAt": generated, "briefings": entries}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"OK: {len(entries)} 号を index.json に書きました（最新 {entries[0]['date'] if entries else 'なし'}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
