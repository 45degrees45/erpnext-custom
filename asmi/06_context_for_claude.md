# Context for Claude — ASMI ERPNext Project

## What you are helping with
Custom ERPNext v15 app development for ASMI (Al Shehab Metal Industries).

## Environment
- Bench: `/home/jo/frappe-bench`
- Apps: `asmi` (v1, quotation), `asmi_v2` (procurement + costing)
- Sites: `site1.local`, `vanilla.local` — both on port 8000
- LAN: `http://192.168.1.103:8000`
- ERPNext: 15.101.0 | Frappe: 15.102.0

## Standard commands
```bash
# Start bench
cd /home/jo/frappe-bench && bench start

# Migrate + rebuild after changes
bench --site site1.local migrate
bench build --app asmi_v2
bench --site site1.local clear-cache

# Check logs
tail -f /home/jo/frappe-bench/logs/web.error.log
```

## Key rules
- Always migrate both sites after doctype JSON changes
- Fix at JSON level (not Property Setter) for portability
- Child table fields need explicit `columns` values or grid falls back to popup
- Global search only indexes parent doctype fields — use hidden aggregate fields for child content

## Focus areas
- Procurement flow: Purchase Enquiry → LPO
- Costing flow: Job Costing with Labour + Material
- Receipt Voucher for payments

## Bug handling (read this every session)
Bugs are tracked in `07_bugs.md` (synced from the Google Sheet `07_bugs` tab).

**At the start of every session:**
1. Read `07_bugs.md`
2. List any bugs with Status = Open to the user
3. Ask which one to work on, or proceed with the user's stated task

**Bug workflow:**
- User adds bugs directly to the Google Sheet (Date + Description in plain language + Status: Open)
- Claude reads the Description, investigates the root cause, and fixes it
- After fixing, update Status to Fixed in `07_bugs.md` and run `python3 sheets_sync.py push` to sync back to the sheet
- Do not ask the user to fill in structured fields — the raw Description is enough

**If the user reports a bug or feature request in the chat:**
- Immediately append it to `07_bugs.md` as a new row (next Bug #, today's date, description, Status: Open)
- Then run `python3 sheets_sync.py push` to sync to the Google Sheet
- Then proceed to fix/implement it
- This applies to any message that describes a problem, unexpected behaviour, or a new feature request — do not wait to be asked to log it
