import logging
from bidi.algorithm import get_display
import arabic_reshaper
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from basic_reference_helper import table_data
import sys
import os

# Logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Resource path helper (bundle-safe)
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

# Register fonts
pdfmetrics.registerFont(TTFont('DejaVu', resource_path('DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('Amiri', resource_path('Amiri-Regular.ttf')))

# Styles
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='WrappedText', fontName='DejaVu', fontSize=7, leading=9, wordWrap='LTR'))
styles.add(ParagraphStyle(name='ArabicText', fontName='Amiri', fontSize=10, leading=12, alignment=2))  # right aligned

# Headers
header = ["#", "Name Arabic", "Esma-ul Husna", "Description Turkish", "Description English"]
numbered_table_data = [header]

# Format Arabic safely
def format_arabic_text(arabic_str):
    try:
        reshaped = arabic_reshaper.reshape(arabic_str)
        return get_display(reshaped)
    except Exception as e:
        logger.error(f"Error reshaping Arabic text: {e}")
        return arabic_str  # fallback

# Add table rows
numbered_table_data += [
    [
        Paragraph(str(row['id']), styles['WrappedText']),
        Paragraph(format_arabic_text(row['Name Arabic']), styles['ArabicText']),
        Paragraph(row['Esma-ul Husna'], styles['WrappedText']),
        Paragraph(row['Description Turkish'], styles['WrappedText']),
        Paragraph(row['Description English'], styles['WrappedText'])
    ]
    for row in table_data
]

# Output file
pdf_file_path = "Esma_ul_Husna_99_Names_Of_Allah.pdf"

doc = SimpleDocTemplate(
    pdf_file_path,
    pagesize=landscape(letter),
    leftMargin=30,
    rightMargin=30,
    topMargin=20,
    bottomMargin=20,
)

# Column widths
base_col_widths = [25, 50, 70, 100, 120, 20, 25, 50, 70, 100, 100]

# Wrap long text
wrapped_table_data = [
    [
        Paragraph(str(cell), styles["WrappedText"]) if isinstance(cell, str) else cell
        for cell in row
    ]
    for row in numbered_table_data
]

# Odd/even split
odd_rows = [row for row in wrapped_table_data[1:] if int(row[0].text.strip()) % 2 != 0]
even_rows = [row for row in wrapped_table_data[1:] if int(row[0].text.strip()) % 2 == 0]

# Calculate rows per page
def calculate_rows_per_page(page_height, row_height, top_margin, bottom_margin):
    available = page_height - top_margin - bottom_margin
    return max(1, int(available // row_height))

# Optimize pages
def optimize_page_utilization(pages, max_rows):
    optimized = []
    for i, page in enumerate(pages):
        if i == len(pages) - 1 and len(page) < max_rows // 2:
            if optimized:
                prev = optimized.pop()
                optimized.append(prev + page)
            else:
                optimized.append(page)
        else:
            optimized.append(page)
    return optimized

# Create combined pages
def create_combined_pages(odd_rows, even_rows, max_rows_per_page):
    pages = []
    while odd_rows or even_rows:
        left = odd_rows[:max_rows_per_page]
        right = even_rows[:max_rows_per_page]
        odd_rows = odd_rows[max_rows_per_page:]
        even_rows = even_rows[max_rows_per_page:]

        max_len = max(len(left), len(right))
        left += [[""] * len(header)] * (max_len - len(left))
        right += [[""] * len(header)] * (max_len - len(right))

        combined = [l + [""] + r for l, r in zip(left, right)]
        pages.append(combined)
    return pages

# Table style
table_style = TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ("FONTNAME", (1, 1), (1, -1), "Amiri"),
    ("FONTNAME", (0, 0), (-1, -1), "DejaVu"),
    ("FONTSIZE", (0, 0), (-1, -1), 7),
    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
])

# Dynamic backgrounds (divider inverted)
def dynamic_row_backgrounds(num_rows):
    row_styles = []
    for i in range(1, num_rows + 1):
        base_color = colors.white if i % 2 != 0 else colors.lightgrey
        divider_color = colors.lightgrey if base_color == colors.white else colors.white
        row_styles.append(("BACKGROUND", (0, i), (4, i), base_color))
        row_styles.append(("BACKGROUND", (6, i), (-1, i), base_color))
        row_styles.append(("BACKGROUND", (5, i), (5, i), divider_color))
    return row_styles

# Build pages
page_height = letter[0]
row_height = 18
rows_per_page = calculate_rows_per_page(page_height, row_height, doc.topMargin, doc.bottomMargin)

try:
    pages = create_combined_pages(odd_rows, even_rows, rows_per_page)
    pages = optimize_page_utilization(pages, rows_per_page)
except Exception as e:
    logger.critical(f"Error building pages: {e}")
    sys.exit(1)

# Add tables
elements = [
    Paragraph("Esma-ül Hüsna (99 Names of Allah swt)", styles["Title"]),
    Spacer(1, 10),
]
for page in pages:
    try:
        page_with_header = [header + [""] + header] + page
        table = Table(page_with_header, colWidths=base_col_widths)
        num_rows = len(page_with_header) - 1
        for s in dynamic_row_backgrounds(num_rows):
            table_style.add(*s)
        table.setStyle(table_style)
        table.repeatRows = 1
        elements.append(table)
        elements.append(PageBreak())
    except Exception as e:
        logger.error(f"Error adding page: {e}")

# Build PDF
try:
    doc.build(elements)
    logger.info(f"✅ PDF created successfully: {pdf_file_path}")
except Exception as e:
    logger.critical(f"Failed to build PDF: {e}")
    sys.exit(1)
