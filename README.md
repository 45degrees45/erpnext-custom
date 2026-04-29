# ERPNext Custom — ASMI

Custom ERPNext v15 apps for **ASMI (Al Shehab Metal Industries)**, covering quotation/selling, procurement, job costing, and payment receipt workflows built on the Frappe framework.

## Apps

| App | Purpose |
|-----|---------|
| `asmi` (v1) | Quotation / Selling — custom quotation form with inline item editing and global search |
| `asmi_v2` | Procurement + Job Costing — Purchase Enquiry → LPO flow, Job Costing, Receipt Voucher |

## Architecture

See [docs/architecture.md](docs/architecture.md) for the full architecture diagram.

## Tech Stack

- ERPNext v15 / Frappe 15
- Python · MariaDB · Redis
- Cloudflare Tunnel (public access)

## Running Locally

```bash
cd /home/jo/frappe-bench
bench start
# Access at http://site1.local:8000 or http://192.168.1.103:8000
```

## Project Docs

Documentation is synced with Google Sheets via `asmi/sheets_sync.py`:

```bash
python3 asmi/sheets_sync.py push   # upload .md files to Sheets
python3 asmi/sheets_sync.py pull   # pull changes back to .md files
```
