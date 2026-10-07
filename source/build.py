#!/usr/bin/env python3
"""
build.py - inject a table inventory (tables.json or .csv) into template.html -> one self-contained HTML file.

    python3 build.py                                   # tables.json -> commission_table_explorer.html
    python3 build.py --data my_real_tables.json --out landscape.html
    python3 build.py --data my_tables.csv              # CSV also accepted (fk_refs ';'-separated)

Minimum fields per table: name, folder, type, rows.  Optional: module, owner, variant, columns, size_mb,
indexes, has_pk, partitioned, growth_per_month, created, last_updated (YYYY-MM-DD), fk_refs, derived_from, description.
"""
import argparse, csv, json, os
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
NUM = {"rows": int, "columns": int, "indexes": int, "growth_per_month": int, "size_mb": float}
BOOL = {"has_pk", "partitioned"}


def load_csv(path):
    tables = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            t = {}
            for k, v in r.items():
                v = (v or "").strip()
                if k in NUM:
                    t[k] = NUM[k](float(v)) if v else None
                elif k in BOOL:
                    t[k] = None if v == "" else v.lower() in ("1", "true", "yes", "y", "t")
                elif k == "fk_refs":
                    t[k] = [x for x in v.replace(",", ";").split(";") if x]
                else:
                    t[k] = v or None
            tables.append(t)
    return {"meta": {"title": os.path.basename(path), "synthetic": False, "source": os.path.basename(path)}, "tables": tables}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=os.path.join(HERE, "tables.json"))
    ap.add_argument("--template", default=os.path.join(HERE, "template.html"))
    ap.add_argument("--out", default=os.path.join(HERE, "commission_table_explorer.html"))
    a = ap.parse_args()
    if a.data.lower().endswith(".csv"):
        payload = load_csv(a.data)
    else:
        with open(a.data, encoding="utf-8") as f:
            payload = json.load(f)
        if isinstance(payload, list):
            payload = {"meta": {}, "tables": payload}
    payload.setdefault("meta", {})
    payload["meta"]["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    # compact JSON; escape '</' so the data can never close the <script> tag
    blob = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    with open(a.template, encoding="utf-8") as f:
        html = f.read()
    assert "__TABLE_DATA__" in html, "placeholder __TABLE_DATA__ missing from template"
    html = html.replace("__TABLE_DATA__", blob, 1)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {a.out}  ({os.path.getsize(a.out)/1024:.0f} KB, {len(payload['tables'])} tables)")


if __name__ == "__main__":
    main()
