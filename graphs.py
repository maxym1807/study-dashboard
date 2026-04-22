import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np


class Graphs:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def create_subject_bar_chart(self):
        grades = self.data_manager.grades
        if not grades:
            return None

        subject_avg = defaultdict(list)
        for g in grades:
            subject_avg[g['subject']].append(g['grade'])

        subjects = []
        averages = []
        colors = []

        for subj, marks in sorted(subject_avg.items()):
            avg = sum(marks) / len(marks)
            subjects.append(subj)
            averages.append(avg)
            if avg >= 10:
                colors.append("#22c55e")
            elif avg >= 7:
                colors.append("#eab308")
            elif avg >= 4:
                colors.append("#f97316")
            else:
                colors.append("#ef4444")

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(subjects, averages, color=colors, edgecolor='black', linewidth=0.8)

        ax.set_ylabel('Середній бал', fontsize=12)
        ax.set_title('Середній бал по предметах', fontsize=16, pad=20)
        ax.set_ylim(0, 12.5)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + 0.25,
                    f'{height:.2f}', ha='center', va='bottom',
                    fontsize=11, fontweight='bold')

        plt.xticks(rotation=15, ha='right', fontsize=11)
        plt.yticks(np.arange(0, 13, 1))

        fig.tight_layout()
        return fig
