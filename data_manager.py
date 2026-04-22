import json
import os
from datetime import datetime
from collections import defaultdict

class DataManager:
    def __init__(self, grades_file="data/grades.json", goals_file="data/goals.json"):
        self.grades_file = grades_file
        self.goals_file = goals_file
        self.ensure_data_folder()
        self.grades = self.load_grades()
        self.goals = self.load_goals()

    def ensure_data_folder(self):
        if not os.path.exists("data"):
            os.makedirs("data")

    def load_grades(self):
        try:
            with open(self.grades_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def load_goals(self):
        try:
            with open(self.goals_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def save_grades(self):
        with open(self.grades_file, "w", encoding="utf-8") as f:
            json.dump(self.grades, f, ensure_ascii=False, indent=2)

    def save_goals(self):
        with open(self.goals_file, "w", encoding="utf-8") as f:
            json.dump(self.goals, f, ensure_ascii=False, indent=2)

    def add_grade(self, subject, grade, work_type=""):
        entry = {
            "date": datetime.now().strftime("%d.%m.%Y"),
            "subject": subject,
            "grade": int(grade),
            "type": work_type
        }
        self.grades.append(entry)
        self.save_grades()
        return entry

    def add_goal(self, name, target):
        entry = {
            "name": name,
            "target": float(target),
            "current_avg": 0.0,
            "date_added": datetime.now().strftime("%d.%m.%Y")
        }
        self.goals.append(entry)
        self.save_goals()
        return entry
