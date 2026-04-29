#!/usr/bin/env python3
"""
ASMI Project ↔ Google Sheets sync.

Usage:
    python3 sheets_sync.py push    # Upload all .md files to Google Sheets
    python3 sheets_sync.py pull    # Pull any changes from Sheets back to .md files

Each .md file gets its own worksheet tab (named after the file, without .md extension).
07_bugs is a special case: stored as columns in the sheet, markdown table in the .md file.

SETUP (one-time):
    Share the Google Sheet with:
        claude-code-feb-28-2026@myjyotishmitra.iam.gserviceaccount.com
    (Give it Editor access)
"""

import sys
import pathlib
import gspread
from google.oauth2.service_account import Credentials

# ─── CONFIG ────────────────────────────────────────────────────────────────
SPREADSHEET_ID = "17KFir-EsxhB-ag7h4SVs8TdD8ctpVa6Z4IdXg8KJcbM"
PROJECT_DIR = pathlib.Path(__file__).parent
SERVICE_ACCOUNT_FILE = pathlib.Path("/home/jo/claude_projects/credentials.json")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]

# .md files to sync — filename without .md = sheet tab name
MD_FILES = [
    "00_overview",
    "01_requirements",
    "02_progress",
    "03_next_steps",
    "04_decisions",
    "05_debug_log",
    "06_context_for_claude",
    "07_bugs",
]

# Sheets that use columnar (table) format instead of line-by-line
TABLE_SHEETS = {"07_bugs"}

BUG_COLUMNS = ["Bug #", "Date", "Description", "Status"]
# ───────────────────────────────────────────────────────────────────────────


def get_sheet():
    creds = Credentials.from_service_account_file(
        str(SERVICE_ACCOUNT_FILE), scopes=SCOPES
    )
    client = gspread.authorize(creds)
    return client.open_by_key(SPREADSHEET_ID)


def ensure_tab(sh, existing_tabs, name, rows, cols):
    if name in existing_tabs:
        ws = existing_tabs[name]
        ws.clear()
        if ws.row_count < rows:
            ws.resize(rows=rows)
        return ws
    return sh.add_worksheet(title=name, rows=rows, cols=cols)


# ── Markdown table helpers ──────────────────────────────────────────────────

def parse_md_table(md_path):
    """Parse a markdown table from 07_bugs.md → list of row dicts."""
    lines = md_path.read_text(encoding="utf-8").splitlines()
    rows = []
    header_seen = False
    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not header_seen:
            header_seen = True  # first pipe-line is the header
            continue
        if all(c.replace("-", "").replace(":", "") == "" for c in cells):
            continue  # separator row
        if len(cells) < len(BUG_COLUMNS):
            cells += [""] * (len(BUG_COLUMNS) - len(cells))
        rows.append(cells[: len(BUG_COLUMNS)])
    return rows


def build_md_table(data_rows):
    """Build 07_bugs.md content from list-of-lists coming from the sheet."""
    sep = "|" + "|".join(["---"] * len(BUG_COLUMNS)) + "|"
    header = "|" + "|".join(BUG_COLUMNS) + "|"
    lines = ["# ASMI — Bug Reports", "", header, sep]
    for row in data_rows:
        # Pad/trim to correct number of columns
        cells = list(row) + [""] * len(BUG_COLUMNS)
        cells = cells[: len(BUG_COLUMNS)]
        lines.append("|" + "|".join(cells) + "|")
    lines.append("")  # trailing newline
    return "\n".join(lines)


# ── Push ────────────────────────────────────────────────────────────────────

def push_doc(sh, existing_tabs, name, md_path):
    """Push a documentation .md (line-per-row in column A)."""
    lines = md_path.read_text(encoding="utf-8").splitlines()
    sheet_rows = [[line] for line in lines] or [[""]]
    ws = ensure_tab(sh, existing_tabs, name, rows=max(len(sheet_rows) + 20, 100), cols=1)
    ws.update(sheet_rows, "A1", value_input_option="RAW")
    print(f"  [PUSH] {name}.md → '{name}' tab  ({len(lines)} lines)")


BUG_COL_WIDTHS = [60, 100, 580, 120]
# Bug#  Date  Description  Status


def push_bugs(sh, existing_tabs, name, md_path):
    """Push 07_bugs.md as a columnar table."""
    data_rows = parse_md_table(md_path)
    sheet_rows = [BUG_COLUMNS] + data_rows  # header row + data
    ws = ensure_tab(sh, existing_tabs, name, rows=max(len(sheet_rows) + 20, 100), cols=len(BUG_COLUMNS))
    ws.update(sheet_rows, "A1", value_input_option="RAW")

    # Bold + freeze the header row
    last_col = chr(ord("A") + len(BUG_COLUMNS) - 1)
    ws.format(f"A1:{last_col}1", {"textFormat": {"bold": True}})
    ws.freeze(rows=1)

    # Set column widths via Sheets API batchUpdate
    sh.batch_update({
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": ws.id,
                        "dimension": "COLUMNS",
                        "startIndex": i,
                        "endIndex": i + 1,
                    },
                    "properties": {"pixelSize": width},
                    "fields": "pixelSize",
                }
            }
            for i, width in enumerate(BUG_COL_WIDTHS)
        ]
    })

    print(f"  [PUSH] {name}.md → '{name}' tab  ({len(data_rows)} bug rows, {len(BUG_COLUMNS)} columns)")


def push():
    print("Pushing local .md files → Google Sheets...")
    sh = get_sheet()
    existing_tabs = {ws.title: ws for ws in sh.worksheets()}

    for name in MD_FILES:
        md_path = PROJECT_DIR / f"{name}.md"
        if not md_path.exists():
            print(f"  [SKIP] {name}.md not found locally")
            continue
        if name in TABLE_SHEETS:
            push_bugs(sh, existing_tabs, name, md_path)
        else:
            push_doc(sh, existing_tabs, name, md_path)

    print("Done.\n")


# ── Pull ────────────────────────────────────────────────────────────────────

def pull_doc(ws, name, md_path):
    """Pull a documentation tab (column A lines → .md file)."""
    rows = ws.col_values(1)
    while rows and not rows[-1].strip():
        rows.pop()
    content = "\n".join(rows) + "\n"
    if md_path.exists() and md_path.read_text(encoding="utf-8") == content:
        print(f"  [OK]   {name}.md — no changes")
        return 0
    md_path.write_text(content, encoding="utf-8")
    print(f"  [PULL] {name}.md ← '{name}' tab  ({len(rows)} lines)")
    return 1


def pull_bugs(ws, name, md_path):
    """Pull 07_bugs columnar tab → markdown table in .md file."""
    all_rows = ws.get_all_values()
    # Skip header row (row 0 = BUG_COLUMNS), take data rows
    data_rows = [r for r in all_rows[1:] if any(c.strip() for c in r)]
    content = build_md_table(data_rows)
    if md_path.exists() and md_path.read_text(encoding="utf-8") == content:
        print(f"  [OK]   {name}.md — no changes")
        return 0
    md_path.write_text(content, encoding="utf-8")
    print(f"  [PULL] {name}.md ← '{name}' tab  ({len(data_rows)} bug rows)")
    return 1


def pull():
    print("Pulling Google Sheets → local .md files...")
    sh = get_sheet()
    existing_tabs = {ws.title: ws for ws in sh.worksheets()}
    updated = 0

    for name in MD_FILES:
        if name not in existing_tabs:
            print(f"  [SKIP] Sheet tab '{name}' not in spreadsheet")
            continue
        ws = existing_tabs[name]
        md_path = PROJECT_DIR / f"{name}.md"
        if name in TABLE_SHEETS:
            updated += pull_bugs(ws, name, md_path)
        else:
            updated += pull_doc(ws, name, md_path)

    print(f"Done. {updated} file(s) updated.\n")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("push", "pull"):
        print("Usage: python3 sheets_sync.py [push|pull]")
        sys.exit(1)
    {"push": push, "pull": pull}[sys.argv[1]]()


if __name__ == "__main__":
    main()
