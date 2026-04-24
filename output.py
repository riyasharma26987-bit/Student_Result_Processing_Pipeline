import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm


COLS        = ["rank", "roll_number", "name", "branch", "percentage", "gpa", "grade"]
COL_HEADERS = ["Rank", "Roll No", "Name", "Branch", "Percentage", "GPA", "Grade"]


def export_csv(df: pd.DataFrame, path: str):
    df[COLS].to_csv(path, index=False)
    print(f"[7] CSV exported → {path}")


def export_pdf(df: pd.DataFrame, path: str):
    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        leftMargin=1.5*cm,
        rightMargin=1.5*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("Student Merit List", styles["Title"]))
    elements.append(Spacer(1, 0.5*cm))

    # Table data
    data = [COL_HEADERS]
    for _, row in df[COLS].iterrows():
        data.append([
            str(row["rank"]),
            str(int(row["roll_number"])),
            str(row["name"]),
            str(row["branch"]),
            f"{row['percentage']:.2f}%",
            str(row["gpa"]),
            str(row["grade"]),
        ])

    table = Table(data, colWidths=[1.5*cm, 2*cm, 5*cm, 2.5*cm, 3*cm, 2*cm, 2*cm])
    table.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0),  colors.HexColor("#1e293b")),
        ("TEXTCOLOR",      (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",       (0, 0), (-1, 0),  10),
        ("ALIGN",          (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
        ("FONTNAME",       (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",       (0, 1), (-1, -1), 9),
        ("GRID",           (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("TOPPADDING",     (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 6),
    ]))

    elements.append(table)
    doc.build(elements)
    print(f"[7] PDF exported → {path}")