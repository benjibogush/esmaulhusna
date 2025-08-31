

import logging
from bidi.algorithm import get_display
import arabic_reshaper
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import sys
import os
from helper import load_esma_with_references

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

pdfmetrics.registerFont(TTFont('DejaVu', resource_path('DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('Amiri', resource_path('Amiri-Regular.ttf')))


# Font registration
# pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
# pdfmetrics.registerFont(TTFont('Amiri', 'Amiri-Regular.ttf'))

# Styles
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Arabic', fontName='Amiri', fontSize=8, leading=10, wordWrap='RTL'))
styles.add(ParagraphStyle(name='NormalSmall', fontName='DejaVu', fontSize=6.5, leading=8, wordWrap='LTR'))
styles.add(ParagraphStyle(name='TitleCentered', fontName='DejaVu', fontSize=14, alignment=1, spaceAfter=10))

# PDF setup
pdf_file_path = "Esma_ul_Husna_with_References.pdf"
doc = SimpleDocTemplate(
    pdf_file_path,
    pagesize=landscape(letter),
    leftMargin=25,
    rightMargin=25,
    topMargin=15,
    bottomMargin=15,
)

# Header row
header = ["#", "Name Arabic", "Transliteration", "Description Turkish", "Description English", "References"]

# Load data
esma_list = load_esma_with_references()

# Prepare table content
table_data = [header]

for item in esma_list:
    name_arabic = item.get("Name_Arabic", "")
    reshaped_arabic = get_display(arabic_reshaper.reshape(name_arabic))
    references = item.get("References", {})
    ref_list = [f"{k}: {v}" for k, v in references.items()]
    ref_para = Paragraph("<br/>".join(ref_list), styles["NormalSmall"])

    table_data.append([
        str(item.get("id", "")),
        Paragraph(reshaped_arabic, styles['Arabic']),
        Paragraph(item.get("Name_English", ""), styles['NormalSmall']),
        Paragraph(item.get("Description_Turkish", ""), styles['NormalSmall']),
        Paragraph(item.get("Description_English", ""), styles['NormalSmall']),
        ref_para
    ])

# Dynamic column widths based on proportions
page_width, _ = landscape(letter)
usable_width = page_width - doc.leftMargin - doc.rightMargin

col_ratios = [0.05, 0.13, 0.15, 0.22, 0.25, 0.20]
col_widths = [usable_width * r for r in col_ratios]

# Table styling
table_style = TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.3, colors.black),
    ("FONTNAME", (0, 0), (-1, -1), "DejaVu"),
    ("FONTNAME", (1, 1), (1, -1), "Amiri"),  # Arabic
    ("FONTSIZE", (0, 0), (-1, -1), 6.5),
    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.darkblue),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.whitesmoke]),
])

# Build document elements
elements = [
    Paragraph("Esma-ül Hüsna (99 Names of Allah SWT)", styles["TitleCentered"]),
    Spacer(1, 6),
    Table(table_data, colWidths=col_widths, style=table_style, repeatRows=1)
]

# Create PDF
try:
    doc.build(elements)
    logger.info(f"PDF generated successfully: {pdf_file_path}")
except Exception as e:
    logger.critical(f"PDF generation failed: {e}")








# import logging
# from bidi.algorithm import get_display
# import arabic_reshaper
# from reportlab.lib.pagesizes import letter, landscape
# from reportlab.lib import colors
# from reportlab.platypus import (
#     SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
# )
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase import pdfmetrics

# from helper import load_esma_with_references

# # Logging setup
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# # Font registration
# pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
# pdfmetrics.registerFont(TTFont('Amiri', 'Amiri-Regular.ttf'))

# # Styles
# styles = getSampleStyleSheet()
# styles.add(ParagraphStyle(name='Arabic', fontName='Amiri', fontSize=10, leading=12, wordWrap='RTL'))
# styles.add(ParagraphStyle(name='NormalSmall', fontName='DejaVu', fontSize=7, leading=9, wordWrap='LTR'))

# # PDF output
# pdf_file_path = "Esma_ul_Husna_with_References.pdf"
# doc = SimpleDocTemplate(
#     pdf_file_path,
#     pagesize=landscape(letter),
#     leftMargin=30,
#     rightMargin=30,
#     topMargin=20,
#     bottomMargin=20,
# )

# # Header row
# header = ["#", "Name Arabic", "Transliteration", "Description Turkish", "Description English", "References"]

# # Load merged data
# esma_list = load_esma_with_references()

# # Table content
# table_data = [header]

# for item in esma_list:
#     name_arabic = item.get("Name_Arabic", "")
#     arabic = get_display(arabic_reshaper.reshape(name_arabic))

#     references = item.get("References", {})
#     ref_list = [f"{k}: {v}" for k, v in references.items()]
#     ref_para = Paragraph("<br/>".join(ref_list), styles["NormalSmall"])

#     table_data.append([
#         str(item.get("id", "")),
#         Paragraph(arabic, styles['Arabic']),
#         Paragraph(item.get("Name_English", ""), styles['NormalSmall']),
#         Paragraph(item.get("Description_Turkish", ""), styles['NormalSmall']),
#         Paragraph(item.get("Description_English", ""), styles['NormalSmall']),
#         ref_para
#     ])

# # Table style
# table_style = TableStyle([
#     ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
#     ("FONTNAME", (0, 0), (-1, -1), "DejaVu"),
#     ("FONTNAME", (1, 1), (1, -1), "Amiri"),  # Arabic column
#     ("FONTSIZE", (0, 0), (-1, -1), 7),
#     ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
#     ("ALIGN", (0, 0), (-1, -1), "CENTER"),
#     ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
# ])

# # Column widths
#  col_widths = [25, 50, 70, 100, 120, 100]
 

# # Build elements
# elements = [
#     Paragraph("Esma-ül Hüsna (99 Names of Allah SWT)", styles["Title"]),
#     Spacer(1, 10),
#     Table(table_data, colWidths=col_widths, style=table_style, repeatRows=1),
# ]

# # Generate PDF
# try:
#     doc.build(elements)
#     logger.info(f"PDF generated: {pdf_file_path}")
# except Exception as e:
#     logger.critical(f"Failed to generate PDF: {e}")
