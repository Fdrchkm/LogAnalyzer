import re
def analyze_logs(logs):
    for log in logs:
        is_evtx = False
        if isinstance(log, str):
            text = log
            if "<Event" in text and "</Event>" in text:
                is_evtx = True
        elif isinstance(log, dict):
            text = " ".join(str(v) for v in log.values())
        else:
            continue
        
        text_upper = text.upper()
        level = None
        description = ""
        event_id = "Не знайдено"
        has_event_id = False  
        

        date_time = "Не знайдено"
        date_match = re.search(r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})", text)
        if date_match:
            date_time = date_match.group(1)

        if "NO FAILED" in text_upper:
            continue
        
        if is_evtx:
            has_event_id = True
            level_match = re.search(r"<Level>(\d)</Level>", text)
            if level_match:
                l = level_match.group(1)
                if l == "1":
                    level = "CRITICAL"
                    description = "Критична помилка в роботі системи"
                elif l == "2":
                    level = "ERROR"
                    description = "Системна помилка або збій системи, входу"
                elif l == "3":
                    level = "WARNING"
                    description = "Потенційно небезпечна подія / попередження"
            
            id_match = re.search(r"<EventID.*?>(.*?)</EventID>", text)
            if id_match:
                event_id = id_match.group(1)

            time_match = re.search(r'SystemTime=["\']([^"\']+)["\']', text)
            if time_match:
                date_time = time_match.group(1).replace("T", " ").split(".")[0]
        else:
            if re.search(r"\bCRITICAL\b", text_upper):
                level = "CRITICAL"
                description = "Критичний апаратний збій або аварійне завершення роботи"
            elif re.search(r"\bERROR\b", text_upper):
                level = "ERROR"
                description = "Помилка конфігурації або внутрішній збій системи"
            elif re.search(r"\bWARNING\b|\bALERT\b", text_upper):
                level = "WARNING"
                description = "Потенційно небезпечна подія або попередження"
            elif re.search(r"\bFAILED\b|\bFAILURE\b", text_upper):
                level = "FAILED"
                description = "Невдала спроба доступу або помилка автентифікації"

        if level:
            source = detect_source(text_upper)
            yield {
                "level": level,
                "source": source,
                "description": description,
                "event_id": event_id,
                "has_event_id": has_event_id, 
                "date_time": date_time,
                "is_evtx": is_evtx,
                "raw_log": text.strip()
            }

def detect_source(text_upper):
    security_keywords = ["SECURITY", "AUTH", "LOGIN", "ACCESS", "DENIED", "UNAUTHORIZED"]
    system_keywords = ["SYSTEM", "KERNEL", "SERVICE", "OS", "DRIVER", "PROCESS"]
    
    for word in security_keywords:
        if word in text_upper:
            return "SECURITY"
    for word in system_keywords:
        if word in text_upper:
            return "SYSTEM"
    return "UNKNOWN"