# ASMI — Decisions Log

## [2026-03-22] Built asmi v1 as separate custom app
**Reason**: Keeps ASMI customizations isolated from core ERPNext. Easier to migrate/upgrade.

## [2026-03-22] Used `description_index` hidden field for search
**Reason**: ERPNext global search indexes parent doctype fields only, not child table fields.  
Workaround: aggregate child descriptions into a hidden parent field and index that.

## [2026-03-22] Fixed grid columns in JSON (not via Property Setter)
**Reason**: Property Setters are DB-level and site-specific. JSON-level fix is permanent and portable across sites.

## [2026-04-15] Created asmi_v2 as a separate app (not extending asmi v1)
**Reason**: v2 covers a different domain (procurement/costing vs selling). Kept separate for clarity.
