"""Build the weekly status .docx from the JSON written by weekly-status.sh.

Usage: build_status_docx.py <input.json> <output.docx>
"""
import json
import sys

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.shared import Pt, RGBColor

COLUMNS = ["Name of Task", "Reference File", "Status", "Comment"]
STATUS_COLORS = {
    "Done": RGBColor(0x1E, 0x7B, 0x34),
    "In progress": RGBColor(0x1F, 0x5F, 0xBF),
    "Designed": RGBColor(0x6A, 0x4C, 0x9C),
    "Not started": RGBColor(0x60, 0x60, 0x60),
    "Blocked": RGBColor(0xB0, 0x2A, 0x2A),
}


def main(src, dest):
    with open(src, encoding="utf-8") as f:
        data = json.load(f)
    tasks = data.get("tasks", [])

    doc = Document()
    section = doc.sections[0]
    section.orientation = WD_ORIENT.LANDSCAPE
    section.page_width, section.page_height = section.page_height, section.page_width

    doc.add_heading("api-pytest — Weekly Status", level=1)
    doc.add_paragraph(
        f"Report date: {data.get('report_date', '')}    "
        f"Week: {data.get('week_start', '')} to {data.get('week_end', '')}"
    )

    counts = {}
    for t in tasks:
        counts[t.get("status", "")] = counts.get(t.get("status", ""), 0) + 1
    summary = ", ".join(f"{k}: {v}" for k, v in counts.items()) or "No tasks found"
    doc.add_paragraph(f"Tasks: {len(tasks)} ({summary})")

    table = doc.add_table(rows=1, cols=len(COLUMNS))
    table.style = "Light Grid Accent 1"
    for cell, title in zip(table.rows[0].cells, COLUMNS):
        cell.text = ""
        run = cell.paragraphs[0].add_run(title)
        run.bold = True

    for t in tasks:
        row = table.add_row().cells
        row[0].text = t.get("name", "")
        row[1].text = "\n".join(t.get("reference_files", [])) or "-"
        status = t.get("status", "")
        run = row[2].paragraphs[0].add_run(status)
        run.bold = True
        if status in STATUS_COLORS:
            run.font.color.rgb = STATUS_COLORS[status]
        row[3].text = t.get("comment", "")

    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(10)

    doc.save(dest)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
