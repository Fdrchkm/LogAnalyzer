import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
from modules.import_log import import_txt, import_csv, import_evtx
from modules.log_analyzer import analyze_logs
from modules.export_log import export_to_pdf

class LogViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("LogAnalyzer")
        self.root.geometry("900x550")
        self.root.minsize(800, 500)
        self.root.configure(bg="#474747")

        self.file_path = None
        self.suspicious_events = []
        self.widgets()

    def widgets(self):
        control_frame = tk.Frame(self.root, bg="#474747")
        control_frame.pack(pady=(20, 15))

        buttons_data = [
            ("📥 Імпортувати", "Формати: .evtx, .txt, .csv", self.import_file),
            ("💻 Згенерувати", "Аналіз подій, фільтрація", self.generate_report),
            ("💾 Експортувати", "Завантаження PDF-звіту", self.export_report)
        ]

        for col, (btn_text, lbl_text, cmd) in enumerate(buttons_data):
            control_frame.columnconfigure(col, weight=1)
            
            btn = tk.Button(
                control_frame, text=btn_text, width=22, height=2,
                font=("Arial", 12, "bold"), bg="white", fg="#000000",
                activebackground="#333333", activeforeground="white", relief=tk.RAISED, bd=2, command=cmd
            )
            btn.grid(row=0, column=col, padx=20, pady=(0, 5))

            lbl = tk.Label(control_frame, text=lbl_text, font=("Arial", 9), bg="#474747", fg="#e4dfdf")
            lbl.grid(row=1, column=col, padx=20)

        self.output = scrolledtext.ScrolledText(
            self.root, font=("Consolas", 10),
            bg="#E7E3E3", fg="#1e1e1e", insertbackground="black"
        )
        self.output.pack(pady=(10, 20), padx=25, fill=tk.BOTH, expand=True)

    def import_file(self):
        filetypes = (("Log files", "*.txt *.csv *.evtx"), ("All files", "*.*"))
        self.file_path = filedialog.askopenfilename(filetypes=filetypes)
        if self.file_path:
            self.output.insert(tk.END, f"Завантажено файл: {self.file_path}\n")
            self.output.see(tk.END)

    def generate_report(self):
        if not self.file_path:
            messagebox.showwarning("Помилка", "Спочатку імпортуйте файл")
            return

        ext = os.path.splitext(self.file_path)[1].lower()
        if ext == ".txt": logs = import_txt(self.file_path)
        elif ext == ".csv": logs = import_csv(self.file_path)
        elif ext == ".evtx": logs = import_evtx(self.file_path)
        else:
            messagebox.showerror("Помилка", "Непідтримуваний формат файлу")
            return

        self.suspicious_events = list(analyze_logs(logs))
        self.output.delete(1.0, tk.END)

        stats = {"CRITICAL": 0, "ERROR": 0, "FAILED": 0, "WARNING": 0}
        for event in self.suspicious_events:
            level = event.get("level", "")
            if level in stats:
                stats[level] += 1
        
        if len(self.suspicious_events) == 0:
            self.output.insert(tk.END, "✅ Підозрілих подій не виявлено.\n")
        else:
            self.output.insert(tk.END, "ЗНАЙДЕНО ПІДОЗРІЛІ ПОДІЇ!!!\n\n")
            self.output.insert(tk.END, f"Загальна кількість: {len(self.suspicious_events)}\n\n")
            self.output.insert(tk.END, f"• Критичні апаратні збої або аварійні завершення (CRITICAL): {stats['CRITICAL']}\n")
            self.output.insert(tk.END, f"• Невдалі спроби доступу або помилки автентифікації (FAILED): {stats['FAILED']}\n")
            self.output.insert(tk.END, f"• Помилки конфігурації або внутрішні збої системи (ERROR): {stats['ERROR']}\n")
            self.output.insert(tk.END, f"• Потенційно небезпечні події або попередження (WARNING): {stats['WARNING']}\n")
            self.output.insert(tk.END, "\n")
            self.output.insert(tk.END, "Для перегляду детального списку виявлених подій завантажте PDF-звіт.\n")
            self.output.see(tk.END)

    def export_report(self):
        if not self.suspicious_events:
            messagebox.showwarning("Помилка", "Немає даних для експорту")
            return

        save_path = filedialog.asksaveasfilename(
            title="Зберегти звіт", defaultextension=".pdf", filetypes=[("PDF файл", "*.pdf")]
        )
        if save_path:
            export_to_pdf(self.suspicious_events, save_path, self.file_path)
            messagebox.showinfo("Готово", f"Звіт збережено:\n{save_path}")

def run_gui():
    root = tk.Tk()
    LogViewer(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
