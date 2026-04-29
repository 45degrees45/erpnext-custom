# ASMI — Progress Log

---

## [2026-03-22] — Session 1 (asmi v1)

### Done
- [x] ERPNext brought up on site1.local + vanilla.local
- [x] `ASMI Quotation` + `ASMI Quotation Item` doctypes created
- [x] Description inline edit fixed (columns set: desc:4, unit:2, qty:1, price:2, amount:1)
- [x] Row 1 alignment fixed via scoped CSS (`asmi_grid_fix.css`)
- [x] Search fields: `quotation_no`, `customer_name`, `description_index`
- [x] Global search enabled — ASMI Quotation inserted into allowed list + index rebuilt
- [x] `description_index` hidden field auto-populated from child row descriptions

### Files Modified
- `apps/asmi/asmi/asmi/doctype/asmi_quotation/asmi_quotation.js`
- `apps/asmi/asmi/asmi/doctype/asmi_quotation_item/asmi_quotation_item.json`
- `apps/asmi/asmi/asmi/doctype/asmi_quotation/asmi_quotation.json`
- `apps/asmi/asmi/asmi/doctype/asmi_quotation/asmi_quotation.py`
- `apps/asmi/asmi/hooks.py`
- `apps/asmi/asmi/public/css/asmi_grid_fix.css`

---

## [2026-04-15] — Session 2 (asmi_v2 discovery)

### Done
- [x] Discovered asmi_v2 app with 4 doctypes built (uncommitted)
- [x] ERPNext brought up, site1.local set as default for LAN access
- [x] Confirmed LAN access at http://192.168.1.103:8000

### asmi_v2 Doctypes Found (uncommitted)
- [x] ASMI Job Costing (+ Labour Row, Material Row child tables)
- [x] ASMI Job Costing Hour Rates (Single)
- [x] ASMI LPO (+ LPO Item)
- [x] ASMI Purchase Enquiry (+ Purchase Enquiry Item)
- [x] ASMI Receipt Voucher (+ print format)
- [x] Quotation Item Search report
- [x] ASMI V2 workspace

### Pending
- [ ] Commit asmi_v2 work to git
- [ ] Test all asmi_v2 doctypes end-to-end
- [ ] Continue building remaining features
