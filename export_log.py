from fpdf import FPDF
import os

def export_to_pdf(events, file_path):
    pdf = FPDF()
    pdf.add_page()

    font_path = os.path.join(
        os.path.dirname(__file__),
        "fonts",
        "DejaVuSans.ttf"
    )
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=16)
    pdf.set_text_color(0, 0, 0) 
    pdf.cell(0, 10, "Звіт аналізу журналів безпеки", ln=True, align="C")
    pdf.ln(5)

    if not events:
        pdf.set_font("DejaVu", size=12)
        pdf.cell(0, 10, "Підозрілих подій не виявлено.", ln=True)
    else:
        for i, event in enumerate(events, start=1):
            level = event["level"]

            if level in ["ERROR", "FAILED"]:
                pdf.set_text_color(200, 0, 0)  
            elif level == "WARNING":
                pdf.set_text_color(200, 100, 0)  
            else:
                pdf.set_text_color(0, 0, 0) 
            
            pdf.set_font("DejaVu", size=12)
            pdf.cell(0, 8, f"{i}. Рівень: {level}", ln=True)
            
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 8, f"   Джерело: {event['source']}", ln=True)
            pdf.multi_cell(0, 8, f"   Опис: {event['description']}")
            pdf.multi_cell(0, 8, f"   Лог: {event['raw_log']}")
            pdf.ln(4)
    
    pdf.output(file_path)