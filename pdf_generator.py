from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import os

FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")

pdfmetrics.registerFont(TTFont("Poppins", os.path.join(FONT_DIR, "Poppins-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Bold", os.path.join(FONT_DIR, "Poppins-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Roboto", os.path.join(FONT_DIR, "Roboto-Regular.ttf")))

def draw_modern_design(c, user_data, width, height):
    """ZAMONAVIY - Ikki ustunli professional dizayn"""
    
    # Chap panel (ko'k rang)
    c.setFillColor(colors.Color(0.2, 0.3, 0.5))
    c.rect(0, 0, 200, height, fill=1)
    
    y_pos = height - 80
    
    # Rasm
    if user_data.get('photo'):
        try:
            img = ImageReader(user_data['photo'])
            c.drawImage(img, 50, y_pos - 100, width=100, height=100, mask='auto')
            y_pos -= 130
        except:
            y_pos -= 30
    
    # Chap paneldagi ma'lumotlar (oq rang)
    c.setFillColor(colors.white)
    
    # Kontakt
    if user_data.get('contact'):
        c.setFont("Poppins-Bold", 11)
        c.drawString(20, y_pos, "ALOQA")
        y_pos -= 20
        c.setFont("Poppins", 9)
        for line in user_data['contact'].split('\n')[:5]:
            c.drawString(20, y_pos, line[:25])
            y_pos -= 15
        y_pos -= 15
    
    # Ko'nikmalar
    if user_data.get('skills'):
        c.setFont("Poppins-Bold", 11)
        c.drawString(20, y_pos, "KO'NIKMALAR")
        y_pos -= 20
        c.setFont("Poppins", 9)
        for line in user_data['skills'].split('\n')[:8]:
            c.drawString(20, y_pos, line[:25])
            y_pos -= 15
        y_pos -= 15
    
    # Linklar
    if user_data.get('links'):
        c.setFont("Poppins-Bold", 11)
        c.drawString(20, y_pos, "LINKLAR")
        y_pos -= 20
        c.setFont("Poppins", 8)
        for line in user_data['links'].split('\n')[:4]:
            c.drawString(20, y_pos, line[:25])
            y_pos -= 15
    
    # O'ng tomon (oq fon)
    y_pos = height - 80
    c.setFillColor(colors.Color(0.2, 0.3, 0.5))
    
    # Ism
    c.setFont("Poppins-Bold", 28)
    c.drawString(230, y_pos, user_data.get('fullname', '')[:20])
    y_pos -= 35
    
    # Lavozim
    c.setFont("Poppins", 14)
    c.drawString(230, y_pos, user_data.get('job', '')[:30])
    y_pos -= 50
    
    c.setFillColor(colors.black)
    
    # Ta'lim
    if user_data.get('education'):
        c.setFont("Poppins-Bold", 12)
        c.drawString(230, y_pos, "TA'LIM")
        y_pos -= 20
        c.setFont("Poppins", 10)
        for line in user_data['education'].split('\n')[:4]:
            c.drawString(230, y_pos, line[:45])
            y_pos -= 15
        y_pos -= 20
    
    # Tajriba
    if user_data.get('experience'):
        c.setFont("Poppins-Bold", 12)
        c.drawString(230, y_pos, "TAJRIBA")
        y_pos -= 20
        c.setFont("Poppins", 10)
        for line in user_data['experience'].split('\n')[:8]:
            if y_pos < 50:
                break
            c.drawString(230, y_pos, line[:45])
            y_pos -= 15

def draw_classic_design(c, user_data, width, height):
    """KLASSIK - An'anaviy biznes stili"""
    
    # Sariq-och fon
    c.setFillColor(colors.Color(0.98, 0.97, 0.94))
    c.rect(0, 0, width, height, fill=1)
    
    y_pos = height - 60
    
    # Yuqorida markazda ism
    c.setFillColor(colors.Color(0.2, 0.1, 0))
    c.setFont("Poppins-Bold", 30)
    name = user_data.get('fullname', '')
    c.drawCentredString(width/2, y_pos, name)
    y_pos -= 30
    
    # Lavozim
    c.setFont("Poppins", 14)
    c.drawCentredString(width/2, y_pos, user_data.get('job', ''))
    y_pos -= 15
    
    # Rasm o'ng yuqori burchakda (kattaroq va pastroq)
    if user_data.get('photo'):
        try:
            img = ImageReader(user_data['photo'])
            c.drawImage(img, width - 150, height - 230, width=120, height=120, mask='auto')
        except:
            pass
    
    # Chiziq (rasm ostidan)
    c.setStrokeColor(colors.Color(0.7, 0.6, 0.5))
    c.setLineWidth(2)
    c.line(100, y_pos, width-100, y_pos)
    y_pos -= 30
    
    # Ma'lumotlar
    sections = [
        ("ALOQA", user_data.get('contact', '')),
        ("TA'LIM", user_data.get('education', '')),
        ("KO'NIKMALAR", user_data.get('skills', '')),
        ("TAJRIBA", user_data.get('experience', '')),
        ("LINKLAR", user_data.get('links', ''))
    ]
    
    for title, content in sections:
        if content and y_pos > 80:
            c.setFont("Poppins-Bold", 13)
            c.drawString(60, y_pos, title)
            y_pos -= 20
            
            c.setFont("Roboto", 10)
            for line in content.split('\n')[:6]:
                if y_pos < 60:
                    break
                c.drawString(60, y_pos, line[:70])
                y_pos -= 14
            y_pos -= 15

def draw_creative_design(c, user_data, width, height):
    """IJODIY - Rangli va zamonaviy"""
    
    # Gradient effect (yashil ranglar)
    for i in range(int(height)):
        shade = 0.85 + (i / height) * 0.1
        c.setFillColor(colors.Color(0.9, shade, 0.9))
        c.rect(0, i, width, 1, fill=1, stroke=0)
    
    y_pos = height - 70
    
    # Yuqorida markazda ism (katta va qora)
    c.setFillColor(colors.Color(0.1, 0.3, 0.1))
    c.setFont("Poppins-Bold", 32)
    c.drawCentredString(width/2, y_pos, user_data.get('fullname', ''))
    y_pos -= 35
    
    # Lavozim
    c.setFont("Poppins", 15)
    c.drawCentredString(width/2, y_pos, user_data.get('job', ''))
    y_pos -= 40
    
    # Rasm markazda (pastroq)
    if user_data.get('photo'):
        try:
            img = ImageReader(user_data['photo'])
            c.drawImage(img, (width-120)/2, y_pos - 130, width=120, height=120, mask='auto')
            y_pos -= 150
        except:
            y_pos -= 20
    
    # Ikki ustun
    left_x = 50
    right_x = width/2 + 20
    
    # Chap ustun
    y_left = y_pos
    c.setFont("Poppins-Bold", 12)
    
    # Ko'nikmalar
    if user_data.get('skills'):
        c.drawString(left_x, y_left, "KO'NIKMALAR")
        y_left -= 18
        c.setFont("Poppins", 9)
        for line in user_data['skills'].split('\n')[:8]:
            c.drawString(left_x, y_left, line[:30])
            y_left -= 13
        y_left -= 10
    
    # Kontakt
    if user_data.get('contact'):
        c.setFont("Poppins-Bold", 12)
        c.drawString(left_x, y_left, "ALOQA")
        y_left -= 18
        c.setFont("Poppins", 9)
        for line in user_data['contact'].split('\n')[:4]:
            c.drawString(left_x, y_left, line[:30])
            y_left -= 13
    
    # O'ng ustun
    y_right = y_pos
    
    # Ta'lim
    if user_data.get('education'):
        c.setFont("Poppins-Bold", 12)
        c.drawString(right_x, y_right, "TA'LIM")
        y_right -= 18
        c.setFont("Poppins", 9)
        for line in user_data['education'].split('\n')[:5]:
            c.drawString(right_x, y_right, line[:30])
            y_right -= 13
        y_right -= 10
    
    # Tajriba
    if user_data.get('experience'):
        c.setFont("Poppins-Bold", 12)
        c.drawString(right_x, y_right, "TAJRIBA")
        y_right -= 18
        c.setFont("Poppins", 9)
        for line in user_data['experience'].split('\n')[:7]:
            if y_right < 50:
                break
            c.drawString(right_x, y_right, line[:30])
            y_right -= 13

def generate_pdf(user_data, pdf_path, design):
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    
    design_lower = design.lower()
    
    if "zamonaviy" in design_lower:
        draw_modern_design(c, user_data, width, height)
    elif "klassik" in design_lower:
        draw_classic_design(c, user_data, width, height)
    else:  # Ijodiy
        draw_creative_design(c, user_data, width, height)
    
    c.save()