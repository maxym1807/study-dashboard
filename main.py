import customtkinter as ctk
from tkinter import messagebox
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

from data_manager import DataManager
from graphs import Graphs

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

MOTIVATIONAL_QUOTES = [
    "Маленькі щоденні зусилля дають великі результати.",
    "Кожна оцінка - це крок до твоєї майбутньої професії.",
    "Не бійся помилок - бійся зупинитися.",
    "Сьогоднішня дисципліна = завтрашня свобода.",
    "Твій майбутній ти дякує тобі за те, що ти робиш зараз.",
    "Математика, фізика та інформатика - твоя основа.",
    "Прогрес виглядає повільно, поки не подивишся назад."
]


class StudyDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Особистий Дашборд Навчання")
        self.geometry("1000x800")
        self.resizable(True, True)

        self.data_manager = DataManager()
        self.graphs = Graphs(self.data_manager)
        self.last_add_time = 0
        self.columns_var = ctk.StringVar(value="2")

        self.create_widgets()

    def create_widgets(self):
        title = ctk.CTkLabel(self, text="Особистий Дашборд Навчання",
                             font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(20, 5))

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)

        self.tabview.add("Головна")
        self.tabview.add("Додати оцінку")
        self.tabview.add("Статистика")
        self.tabview.add("Історія")

        self.create_main_tab()
        self.create_add_grade_tab()
        self.create_stats_tab()
        self.create_history_tab()

    def create_main_tab(self):
        tab = self.tabview.tab("Головна")
        ctk.CTkLabel(tab, text="Загальна статистика",
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        self.main_stats_label = ctk.CTkLabel(tab, text="",
                                             font=ctk.CTkFont(size=17), justify="left")
        self.main_stats_label.pack(pady=20)
        self.quote_label = ctk.CTkLabel(tab, text="",
                                        font=ctk.CTkFont(family="Times New Roman", size=24, slant="italic"),
                                        text_color="#a5b4fc", wraplength=700)
        self.quote_label.pack(pady=40, padx=50)
        self.update_main_stats()

    def update_main_stats(self):
        grades = self.data_manager.grades
        if not grades:
            self.main_stats_label.configure(text="Поки немає оцінок.\nДодайте перші оцінки!")
            self.quote_label.configure(text=random.choice(MOTIVATIONAL_QUOTES))
            return

        total = len(grades)
        avg = sum(g['grade'] for g in grades) / total
        from collections import defaultdict
        subj_avg = defaultdict(list)
        for g in grades:
            subj_avg[g['subject']].append(g['grade'])

        best = max(subj_avg, key=lambda s: sum(subj_avg[s]) / len(subj_avg[s]))
        worst = min(subj_avg, key=lambda s: sum(subj_avg[s]) / len(subj_avg[s]))

        text = f"Оцінок всього: {total}\n"
        text += f"Середній бал: {avg:.2f}\n\n"
        text += f"🏆 Найкращий предмет: {best}\n"
        text += f"📉 Найгірший предмет: {worst}"

        self.main_stats_label.configure(text=text)
        self.quote_label.configure(text=random.choice(MOTIVATIONAL_QUOTES))

    def create_history_tab(self):
        tab = self.tabview.tab("Історія")
        ctk.CTkLabel(tab, text="Історія оцінок",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=15)
        top_frame = ctk.CTkFrame(tab)
        top_frame.pack(fill="x", padx=25, pady=10)

        subjects = ["Всі предмети", "Математика", "Фізика", "Інформатика", "Українська мова",
                    "Англійська мова", "Хімія", "Біологія", "Історія", "Географія"]

        self.history_subject_var = ctk.StringVar(value="Всі предмети")
        ctk.CTkOptionMenu(top_frame, values=subjects, variable=self.history_subject_var,
                          command=lambda _: self.update_history(), width=280).pack(side="left", padx=(0, 20))
        ctk.CTkLabel(top_frame, text="Стовпців:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(10, 5))
        ctk.CTkOptionMenu(top_frame, values=["1", "2", "3"], variable=self.columns_var,
                          command=lambda _: self.update_history(), width=100).pack(side="left")
        self.history_frame = ctk.CTkScrollableFrame(tab)
        self.history_frame.pack(fill="both", expand=True, padx=25, pady=10)
        self.update_history()

    def update_history(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        for i in range(5):
            self.history_frame.grid_columnconfigure(i, weight=0, uniform="")

        grades = self.data_manager.grades
        selected = self.history_subject_var.get()
        columns = int(self.columns_var.get())
        filtered = grades if selected == "Всі предмети" else [g for g in grades if g['subject'] == selected]

        if not filtered:
            ctk.CTkLabel(self.history_frame, text="Оцінок за вибраним предметом немає",
                         font=ctk.CTkFont(size=16)).pack(pady=100)
            return

        for i, entry in enumerate(reversed(filtered[-50:])):
            grade = entry['grade']
            if grade >= 10:
                color = "#22c55e"
                text_color = "white"
            elif grade >= 7:
                color = "#eab308"
                text_color = "white"
            elif grade >= 4:
                color = "#f97316"
                text_color = "white"
            else:
                color = "#ef4444"
                text_color = "white"

            card = ctk.CTkFrame(self.history_frame, fg_color=color, corner_radius=12)

            if columns == 1:
                card.pack(fill="x", pady=6, padx=10)
            else:
                card.grid(row=i // columns, column=i % columns, padx=8, pady=8, sticky="new")

            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(fill="x", padx=14, pady=10)

            ctk.CTkLabel(info_frame, text=entry['date'], text_color=text_color,
                         font=ctk.CTkFont(size=13)).pack(anchor="w")
            ctk.CTkLabel(info_frame, text=entry['subject'], text_color=text_color,
                         font=ctk.CTkFont(size=17, weight="bold")).pack(anchor="w", pady=2)

            info = f"Оцінка: {grade}   |   {entry.get('type', '—')}"
            ctk.CTkLabel(info_frame, text=info, text_color=text_color,
                         font=ctk.CTkFont(size=15)).pack(anchor="w")
            delete_btn = ctk.CTkButton(card, text="🗑", width=30, height=30,
                                       fg_color="#b91c1c", hover_color="#941c1c",
                                       command=lambda e=entry: self.delete_grade(e))
            if columns == 1:
                delete_btn.place(anchor="se", relx=.99, rely=.92)
            elif columns == 2:
                delete_btn.place(anchor="se", relx=.98, rely=.92)
            else:
                delete_btn.place(anchor="se", relx=.97, rely=.92)

        if columns > 1:
            for i in range(columns):
                self.history_frame.grid_columnconfigure(i, weight=1, uniform="card_group")

    def delete_grade(self, entry):
        if messagebox.askyesno("Підтвердження", "Видалити цю оцінку?"):
            self.data_manager.grades.remove(entry)
            self.data_manager.save_grades()
            self.update_main_stats()
            self.update_stats()
            self.update_history()

    def create_add_grade_tab(self):
        tab = self.tabview.tab("Додати оцінку")
        ctk.CTkLabel(tab, text="Додати оцінку",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(10,  5))
        container = ctk.CTkFrame(tab)
        container.pack(padx=20)

        subjects = ["Математика", "Фізика", "Інформатика", "Українська мова",
                    "Англійська мова", "Хімія", "Біологія", "Історія", "Географія"]

        ctk.CTkLabel(container, text="Предмет:", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(0, 5))
        self.subject_var = ctk.StringVar(value=subjects[0])
        ctk.CTkOptionMenu(container, values=subjects, variable=self.subject_var, width=340).pack(pady=(0, 20))

        ctk.CTkLabel(container, text="Оцінка (1-12):", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(0, 5))
        self.grade_var = ctk.StringVar()
        ctk.CTkEntry(container, textvariable=self.grade_var, width=340, height=40).pack(pady=(0, 20))

        ctk.CTkLabel(container, text="Тип роботи:", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(0, 5))
        self.type_var = ctk.StringVar()
        ctk.CTkEntry(container, textvariable=self.type_var, width=340, height=40,
                     placeholder_text="Контрольна, домашня, тест...").pack(pady=(0, 30))

        self.add_button = ctk.CTkButton(container, text="Додати оцінку",
                                        command=self.add_grade, width=340, height=50,
                                        font=ctk.CTkFont(size=16))
        self.add_button.pack()

        self.success_label = ctk.CTkLabel(container, text="", text_color="lightgreen",
                                          font=ctk.CTkFont(size=15))
        self.success_label.pack(pady=15)

    def add_grade(self):
        if time.time() - self.last_add_time < 3:
            self.success_label.configure(text="Зачекайте 3 секунди...", text_color="orange")
            self.grade_var.set("")
            self.type_var.set("")
            return

        try:
            grade = int(self.grade_var.get())
            if not 1 <= grade <= 12:
                raise ValueError
        except:
            messagebox.showerror("Помилка", "Оцінка має бути від 1 до 12!")
            return

        self.data_manager.add_grade(self.subject_var.get(), grade, self.type_var.get())

        self.success_label.configure(text=f"✅ Оцінка {grade} з {self.subject_var.get()} додана!",
                                     text_color="lightgreen")

        self.grade_var.set("")
        self.type_var.set("")

        self.update_main_stats()
        self.update_stats()
        self.update_history()

        self.last_add_time = time.time()
        self.after(3000, lambda: self.success_label.configure(text=""))

    def create_stats_tab(self):
        tab = self.tabview.tab("Статистика")
        ctk.CTkLabel(tab, text="Статистика та графіки",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=15)

        ctk.CTkButton(tab, text="Оновити графіки", command=self.update_stats).pack(pady=8)

        self.stats_frame = ctk.CTkFrame(tab)
        self.stats_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.update_stats()

    def update_stats(self):
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        fig = self.graphs.create_subject_bar_chart()
        if fig:
            canvas = FigureCanvasTkAgg(fig, self.stats_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)


if __name__ == "__main__":
    app = StudyDashboard()
    app.mainloop()
