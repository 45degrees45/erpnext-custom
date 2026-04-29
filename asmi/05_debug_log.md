# ASMI — Debug Log

---

## [2026-03-22] Description field opened Edit Row popup instead of inline edit

**Issue**: Clicking description in ASMI Quotation item grid opened a popup instead of editing inline.

**Root Cause**: All fields in `tabDocField` for ASMI Quotation Item had `columns = 0`. Frappe v15 falls back to Edit Row popup when columns are 0.

**Fix**: Set explicit columns in `asmi_quotation_item.json`:
- description: 4, unit: 2, quantity: 1, price: 2, amount: 1

**Commands to apply fix**:
```bash
bench --site site1.local migrate
bench build --app asmi
bench --site site1.local clear-cache
```

**Verify**:
```sql
SELECT fieldname, columns, in_list_view FROM tabDocField WHERE parent='ASMI Quotation Item';
```

---

## [2026-03-22] Global Search not returning ASMI Quotation records

**Issue**: Searching quotation numbers in global search returned no results.

**Root Cause**: ASMI Quotation was not in the `tabGlobal Search DocType` allow-list.

**Fix**:
```bash
bench --site <site> rebuild-global-search
```
Also inserted ASMI Quotation into allowed_in_global_search for both sites.

---

## [2026-04-15] Global Search not finding descriptions with short terms (MS, 6mm, etc.)

**Issue**: Searching description keywords like "MS", "6mm", "3mm" in global search returned no ASMI Quotation results.

**Root Cause 1 — ft_min_word_len = 4**: MariaDB FULLTEXT (MyISAM) ignores words shorter than 4 characters. Metal terms like "MS" (2), "6mm" (3), "x" (1) were silently dropped from the index.

**Root Cause 2 — Priority #54**: ASMI Quotation was at the last position in `tabGlobal Search DocType`. Frappe's global search fetches top 20 results by FULLTEXT rank — for common metal terms, BOMs/Items fill all 20 slots.

**Fix**:
1. Set `ft_min_word_len = 2` in `/etc/mysql/mariadb.conf.d/frappe.cnf`
2. `sudo systemctl restart mariadb`
3. `REPAIR TABLE __global_search QUICK` (in bench console)
4. Move ASMI Quotation to `idx = 6` in `tabGlobal Search DocType` (both sites)
5. `bench --site site1.local rebuild-global-search` + same for vanilla.local

**Verified**: "MS", "6mm", "MS Plate", "Plate", "Steel", "2500mm" all return ASMI Quotation results.

**Note**: If MariaDB is ever reinstalled or config reset, re-add `ft_min_word_len = 2` to frappe.cnf and repeat steps 2–5.

---
