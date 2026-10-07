# Commission System – Table Landscape Explorer

A single-file, static HTML explorer for an inventory of ~2000 database tables. Open `commission_table_explorer.html` in any modern browser. ECharts and Tabulator load from the jsDelivr CDN, so the page needs internet access. The data itself is embedded in the file.

| File | Purpose |
|---|---|
| `commission_table_explorer.html` | Deliverable: one self-contained page (data inlined) |
| `template.html` | Page source. `__TABLE_DATA__` is replaced at build time |
| `build.py` | Injects `tables.json` (or a CSV) into the template |
| `generate_data.py` | Deterministic synthetic data generator (`--seed`, `--target`) |
| `tables.json` / `tables.csv` | The generated sample dataset |
| `test_page.py`, `test_clicks.py` | Headless-Chrome smoke tests (Playwright) |

Regenerate: `python3 generate_data.py && python3 build.py`

Use real data: `python3 build.py --data my_inventory.csv --out landscape.html`.
The required columns are `name, folder, type, rows`.
The optional columns are `module, owner, variant, columns, size_mb, indexes, has_pk, partitioned, growth_per_month, created, last_updated (YYYY-MM-DD), fk_refs (;-separated), derived_from, description`.
Set `meta.as_of` in the JSON to control the staleness reference date. If it isn't set, the page uses today's date.
