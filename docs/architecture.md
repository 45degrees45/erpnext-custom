# Architecture — ASMI ERPNext Custom

Custom ERPNext v15 apps built for ASMI (Al Shehab Metal Industries) to handle their selling, procurement, job costing, and payment workflows, extending the standard Frappe/ERPNext platform with bespoke doctypes, client-side logic, print formats, and a Google Sheets sync utility for project documentation.

```mermaid
flowchart TD
    subgraph Bench["Frappe Bench — site1.local:8000"]
        direction TB

        subgraph asmi_v1["App: asmi (v1) — Selling"]
            AQ["ASMI Quotation\n(Parent DocType)"]
            AQI["ASMI Quotation Item\n(Child Table)"]
            AQ_JS["asmi_quotation.js\n(inline edit, live amount)"]
            AQ_PY["asmi_quotation.py\n(description_index aggregator)"]
            AQ_CSS["asmi_grid_fix.css\n(grid alignment)"]
            AQ --> AQI
            AQ_JS --> AQ
            AQ_PY --> AQ
            AQ_CSS --> AQ
        end

        subgraph asmi_v2["App: asmi_v2 — Procurement &amp; Costing"]
            PE["ASMI Purchase Enquiry"]
            PEI["Purchase Enquiry Item\n(Child Table)"]
            LPO["ASMI LPO\n(Local Purchase Order)"]
            LPOI["LPO Item\n(Child Table)"]
            JC["ASMI Job Costing"]
            JCL["Job Costing Labour Row\n(Child Table)"]
            JCM["Job Costing Material Row\n(Child Table)"]
            JCH["Job Costing Hour Rates\n(Single DocType — config)"]
            RV["ASMI Receipt Voucher"]
            RV_PRINT["asmi_receipt_voucher_print.html\n(Print Format)"]
            RPT["Quotation Item Search\n(Script Report)"]

            PE --> PEI
            PE -->|convert| LPO
            LPO --> LPOI
            JC --> JCL
            JC --> JCM
            JCH -.->|rates config| JC
            RV --> RV_PRINT
        end

        subgraph Standard["Standard ERPNext / Frappe"]
            GS["Global Search Index"]
            WS["ASMI V2 Workspace"]
        end

        AQ_PY -->|populate description_index| GS
        AQ -.->|searchable via| GS
        asmi_v2 -.->|shortcuts| WS
    end

    subgraph ExternalIntegrations["External Integrations"]
        GSheets["Google Sheets\n(Project Docs Tracker)"]
        SyncScript["asmi/sheets_sync.py\ngspread + Service Account"]
    end

    subgraph ProjectDocs["Local Documentation (.md files)"]
        MD["00_overview · 01_requirements\n02_progress · 03_next_steps\n04_decisions · 05_debug_log\n06_context_for_claude · 07_bugs"]
    end

    MD <-->|push / pull| SyncScript
    SyncScript <-->|Sheets API| GSheets

    subgraph Infra["Infrastructure"]
        MariaDB["MariaDB"]
        Redis["Redis\n(cache + queue)"]
        Gunicorn["Gunicorn\n(25 workers, port 8000)"]
        Socketio["Socket.IO\n(port 9000)"]
        CF["Cloudflare Tunnel\n(public HTTPS access)"]
    end

    Bench --> MariaDB
    Bench --> Redis
    Bench --> Gunicorn
    Bench --> Socketio
    CF --> Gunicorn
```
