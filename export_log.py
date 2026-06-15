import os
import getpass
from datetime import datetime
from fpdf import FPDF

def export_to_pdf(events, file_path, file_name="Не вказано"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    font_dir = os.path.join(os.path.dirname(__file__), "fonts")
    font_regular = os.path.join(font_dir, "DejaVuSans.ttf")
    font_bold = os.path.join(font_dir, "DejaVuSans-Bold.ttf")
    
    pdf.add_font("DejaVu", "", font_regular)
    pdf.add_font("DejaVu", "B", font_bold)
    
    # Заголовок
    pdf.set_font("DejaVu", "B", size=16)
    pdf.set_text_color(20, 40, 80)
    pdf.cell(0, 12, "ЗВІТ АНАЛІЗУ ЖУРНАЛІВ ПОДІЙ", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(4)

    # Метадані
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    try:
        system_user = getpass.getuser()
    except Exception:
        system_user = "Користувач системи"

    pdf.set_font("DejaVu", "B", size=10)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 6, "МЕТАДАНІ ДОКУМЕНТА:", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("DejaVu", size=10)
    pdf.set_fill_color(245, 247, 250)
    
    col_width = 55  
    val_width = 135
    
    pdf.cell(col_width, 6, " Аналізований файл:", border=1, fill=True)
    pdf.cell(val_width, 6, f" {os.path.basename(file_name)}", border=1, new_x="LMARGIN", new_y="NEXT")

    pdf.cell(col_width, 6, " Час\дата створення:", border=1, fill=True)
    pdf.cell(val_width, 6, f" {current_time}", border=1, new_x="LMARGIN", new_y="NEXT")
    
    pdf.cell(col_width, 6, " Користувач:", border=1, fill=True)
    pdf.cell(val_width, 6, f" {system_user}", border=1, new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(6)

    # Статистика
    stats = {"CRITICAL": 0, "ERROR": 0, "WARNING": 0, "FAILED": 0}
    for e in events:
        lvl = e.get("level", "UNKNOWN")
        if lvl in stats:
            stats[lvl] += 1

    pdf.set_font("DejaVu", "B", size=10)
    pdf.cell(0, 6, "ЗВЕДЕНА СТАТИСТИКА ВИЯВЛЕНИХ ПОДІЙ:", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("DejaVu", "B", size=9)
    pdf.set_fill_color(220, 225, 235)
    pdf.cell(47, 6, " Рівень загрози", border=1, fill=True, align="C")
    pdf.cell(47, 6, " Кількість подій", border=1, fill=True, align="C")
    pdf.cell(96, 6, " Статус інциденту", border=1, fill=True, align="C", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("DejaVu", size=9)
    levels_config = [
        ("CRITICAL", stats["CRITICAL"]),
        ("FAILED", stats["FAILED"]),
        ("ERROR", stats["ERROR"]),
        ("WARNING", stats["WARNING"])
    ]
    
    for lvl_name, count in levels_config:
        pdf.cell(47, 6, f" {lvl_name}", border=1, align="C")
        pdf.cell(47, 6, f" {count}", border=1, align="C")
        
        if count > 0:
            if lvl_name == "CRITICAL":
                pdf.set_text_color(220, 0, 0)      # Насичений червоний
            elif lvl_name == "FAILED":
                pdf.set_text_color(130, 0, 0)      # Темно-червоний
            elif lvl_name == "ERROR":
                pdf.set_text_color(180, 40, 40)    # Червоний
            elif lvl_name == "WARNING":
                pdf.set_text_color(210, 140, 0)    # Жовтий 
                
            pdf.cell(96, 6, f"⚠️ Виявлено ({count} шт.)", border=1, new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(50, 50, 50)
        else:
            pdf.set_text_color(0, 120, 0)
            pdf.cell(96, 6, "Норма (не виявлено)", border=1, new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(50, 50, 50)

    pdf.ln(5)
    pdf.set_draw_color(100, 120, 140)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Перелік подій
    pdf.set_font("DejaVu", "B", size=12)
    pdf.set_text_color(20, 40, 80)
    pdf.cell(0, 8, "ДЕТАЛЬНИЙ РЕЄСТР ВИЯВЛЕНИХ ПОДІЙ", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    for i, event in enumerate(events, start=1):
        level = event.get("level", "UNKNOWN")
        is_evtx = event.get("is_evtx", False)

        if level == "CRITICAL":
            pdf.set_text_color(220, 0, 0)
        elif level == "FAILED":
            pdf.set_text_color(130, 0, 0)
        elif level == "ERROR":
            pdf.set_text_color(180, 40, 40)
        elif level == "WARNING":
            pdf.set_text_color(210, 140, 0)
        else:
            pdf.set_text_color(0, 0, 0)
            
        pdf.set_font("DejaVu", "B", size=10)
        pdf.cell(0, 7, f"ПОДІЯ №{i} [{level}]", new_x="LMARGIN", new_y="NEXT")
            
        pdf.set_text_color(40, 40, 40)
        pdf.set_font("DejaVu", size=9.5)
            
        # 1. Дата та час
        pdf.cell(35, 5, "• Дата та час:", new_x="RIGHT", new_y="LAST")
        pdf.set_font("DejaVu", "B", size=9.5)
        pdf.cell(0, 5, f" {event.get('date_time', 'Не знайдено')}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("DejaVu", size=9.5)

        # 2. Ідентифікатор 
        if event.get("has_event_id", False):
            pdf.cell(35, 5, "• Ідентифікатор:", new_x="RIGHT", new_y="LAST")
            pdf.set_font("DejaVu", "B", size=9.5)
            pdf.cell(0, 5, f" Event ID {event.get('event_id', 'Не знайдено')}", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("DejaVu", size=9.5)

        # 3. Джерело події 
        pdf.cell(35, 5, "• Джерело події:", new_x="RIGHT", new_y="LAST")
        pdf.cell(0, 5, f" {event.get('source', 'UNKNOWN')}", new_x="LMARGIN", new_y="NEXT")
        
        # 4. Суть проблеми 
        pdf.cell(35, 5, "• Суть проблеми:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("DejaVu", "B", size=9.5)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(0, 5, f"{event.get('description', 'Опис відсутній')}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("DejaVu", size=9.5)
        pdf.set_text_color(40, 40, 40)
        
        # 5. Рядок логу 
        if is_evtx:
            pdf.set_text_color(120, 120, 120)
            pdf.set_font("DejaVu", size=9)
            pdf.cell(0, 5, "Початковий текст логу приховано через значний обсяг XML-структури.", new_x="LMARGIN", new_y="NEXT")
            pdf.cell(0, 5, "Для детального аналізу інциденту перегляньте початковий файл журналу", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("DejaVu", size=9.5)
        else:
            pdf.set_text_color(90, 90, 90)
            pdf.cell(0, 5, "Первинний рядок логу:", new_x="LMARGIN", new_y="NEXT")
            pdf.multi_cell(0, 4.5, f"{event.get('raw_log', '')}", new_x="LMARGIN", new_y="NEXT")
        
    
        pdf.ln(2)
        pdf.set_draw_color(220, 225, 230)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(3)

    pdf.output(file_path)