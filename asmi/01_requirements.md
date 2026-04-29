# ASMI — Requirements

## Modules to Build

### 1. Quotation (asmi v1 — IN PROGRESS)
- Custom quotation form with item grid
- Inline editing of description field
- Search by quotation no. + description
- **[CRITICAL] Global search must return ASMI Quotation records by description text**
  - Client requirement: staff must be able to type any word from an item description and find the quotation
  - Must work from the top global search bar in ERPNext desk
  - Example: searching "steel pipe" must return all quotations that have "steel pipe" in any item description row

### 2. Purchase Enquiry (asmi_v2 — IN PROGRESS)
- Raise enquiry for items needed
- Child table: items (description, qty, unit)

### 3. LPO — Local Purchase Order (asmi_v2 — IN PROGRESS)
- Convert Purchase Enquiry → LPO
- Child table: items

### 4. Job Costing (asmi_v2 — IN PROGRESS)
- Track cost per job
- Labour rows (hours × rate)
- Material rows (qty × rate)
- Hour Rates config (Single doctype)

### 5. Receipt Voucher (asmi_v2 — IN PROGRESS)
- Payment receipt recording
- Custom print format: `asmi_receipt_voucher_print.html`

### 6. Reports
- Quotation Item Search (done in asmi_v2)

---

## Constraints
- ERPNext v15 / Frappe 15
- Must not break standard ERPNext modules
- Both sites (site1.local + vanilla.local) must stay in sync
