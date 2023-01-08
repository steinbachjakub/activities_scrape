from docx.shared import Pt, RGBColor
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH

def change_styles(document_styles):
    title_style = document_styles.add_style("TitleStyle", WD_STYLE_TYPE.PARAGRAPH)
    title_style.font.name = "Kelson Sans"
    title_style.font.size = Pt(24)
    title_style.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    header_style = document_styles.add_style("HeaderStyle", WD_STYLE_TYPE.PARAGRAPH)
    header_style.font.name = "Lato"
    header_style.font.size = Pt(16)
    header_style.font.bold = True
    header_style.font.color.rgb = RGBColor(0x2E, 0x31, 0x92)
    header_style.paragraph_format.keep_with_next = True
    text_style = document_styles.add_style("TextStyle", WD_STYLE_TYPE.PARAGRAPH)
    text_style.font.name = "Lato"
    text_style.font.size = Pt(11)
    text_style.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    text_style.paragraph_format.keep_with_next = True
    text_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    return title_style, header_style, text_style