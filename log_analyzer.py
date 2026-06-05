import re

def analyze_logs(logs): #функція читання файлу
    for log in logs:
        if isinstance(log, str):
            text = log

        elif isinstance(log, dict):
            text = " ".join(str(v) for v in log.values()) #перетворення словника в текстовий формат
        else:
            continue
        
        text_upper = text.upper()
        level = None
        description = ""

        # Захист від помилкових спрацювань
        if "NO FAILED" in text_upper:
            continue
        
        # Пошук для evtx
        level_match = re.search(r"<Level>(\d)</Level>", text)
        if level_match:
            l = level_match.group(1)
            if l in ["1", "2"]:
                level = "ERROR"
                description = "Критична помилка в роботі системи"
            elif l == "3":
                level = "WARNING"
                description = "Потенційно небезпечна подія"
        
        # Аналіз 
        if not level:
            if re.search(r"\bFAILED\b|\bFAILURE\b", text_upper):
                level = "FAILED"
                description = "Невдала операція або збій автентифікації"

            elif re.search(r"\bERROR\b|\bCRITICAL\b", text_upper):
                level = "ERROR"
                description = "Критична помилка в роботі системи"

            elif re.search(r"\bWARNING\b|\bALERT\b", text_upper):
                level = "WARNING"
                description = "Потенційно небезпечна подія"

        if level:
            source = detect_source(text_upper)
            yield {
                "level": level,
                "source": source,
                "description": description,
                "raw_log": text.strip()
            }

def detect_source(text_upper): #функція пошуку джерела події
    security_keywords = [
        "SECURITY", "AUTH", "LOGIN",
        "ACCESS", "DENIED", "UNAUTHORIZED"
    ]
    system_keywords = [
        "SYSTEM", "KERNEL", "SERVICE",
        "OS", "DRIVER", "PROCESS"
    ]
    for word in security_keywords:
        if word in text_upper:
            return "SECURITY"
        
    for word in system_keywords:
        if word in text_upper:
            return "SYSTEM"
        
    return "UNKNOWN"
