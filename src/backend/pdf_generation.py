import io

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas

__TITLE_FONT_SIZE = 15
__NORMAL_FONT_SIZE = 13
__FONT_NAME = "Helvetica"
__WIDTH, __HEIGHT = A4


def _create_title(c: canvas.Canvas, title: str):
    c.setFont(__FONT_NAME + "-Bold", __TITLE_FONT_SIZE)
    c.drawCentredString(__WIDTH / 2, __HEIGHT - 30, title)
    c.setFont(__FONT_NAME, __NORMAL_FONT_SIZE)


def _create_table(c: canvas.Canvas, headings: list[list[str]], data: dict):
    for k, v in data.items():
        headings.append([str(k), str(v)])

        table = Table(headings, colWidths=[200, 200])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), __FONT_NAME + "-Bold"),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        table_width, table_height = table.wrap(0, 0)
        x = __WIDTH / 2 - table_width / 2
        y = __HEIGHT - 70
        table.wrapOn(c, __WIDTH, __HEIGHT)
        table.drawOn(c, x, y - table_height)


def gen_pdf(title: str, data: dict) -> io.BytesIO:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    _create_title(c, title)
    _create_table(c, [["Id", "Zaliczenie"]], data)
    c.showPage()
    c.save()

    return buffer


if __name__ == "__main__":
    debug_data: dict = {
            "s00001": True,
            "s00002": False,
            "s30593": True
    }

    with open("gen_pdf.pdf", "wb") as f:
        f.write(gen_pdf("Example title", debug_data).getbuffer())
