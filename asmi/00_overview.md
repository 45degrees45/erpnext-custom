# ASMI — Project Overview

**Project**: ASMI (Al Shehab Metal Industries) — Custom ERPNext Modules  
**Bench Path**: `/home/jo/frappe-bench`  
**Sites**: `site1.local:8000`, `vanilla.local:8000`  
**LAN Access**: `http://192.168.1.103:8000`  
**Login**: Administrator / admin

---

## Apps

| App | Branch | Purpose |
|-----|--------|---------|
| `asmi` | develop | Quotation / Selling flow (v1) |
| `asmi_v2` | develop | Procurement + Job Costing (v2, active) |

## Goal

Build a complete custom ERP flow for ASMI covering:
- Quotation (selling)
- Purchase Enquiry → LPO (procurement)
- Job Costing (production/costing)
- Receipt Voucher (payments)

## Current Status

- `asmi` v1: Quotation module working, grid + search fixes done
- `asmi_v2`: 4 doctypes + 1 report built, **uncommitted to git**
