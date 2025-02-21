import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.config import SUBJECTS

class SubjectView:
    TAB_NAME = "科目別統計"
    
    def __init__(self, parent, tracker):
        self.parent = parent
        self.tracker = tracker
        self.setup_view()
    
    def setup_view(self):
        # 科目ごとの統計を計算
        subject_stats = self.calculate_stats()
        self.show_stats_table(subject_stats)
        self.show_stats_graphs(subject_stats)
    
    def calculate_stats(self):
        stats = {}
        for subject in SUBJECTS.keys():
            stats[subject] = {'time': 0, 'exp': 0}
        
        for log in self.tracker.study_log:
            subject = log[2]
            if subject in stats:
                stats[subject]['time'] += log[1]
                stats[subject]['exp'] += log[3]
        
        return stats
    
    def show_stats_table(self, stats):
        # テーブルフレーム
        table_frame = ttk.LabelFrame(self.parent, text="科目別集計")
        table_frame.pack(pady=10, padx=10, fill='x')
        
        # ヘッダー
        headers = ['Subject', 'Total Time (min)', 'Total EXP']
        for col, header in enumerate(headers):
            ttk.Label(table_frame, text=header).grid(row=0, column=col, padx=5, pady=5)
        
        # データ行
        for row, (subject, data) in enumerate(stats.items(), 1):
            ttk.Label(table_frame, text=SUBJECTS[subject]['name_en']).grid(
                row=row, column=0, padx=5, pady=2)
            ttk.Label(table_frame, text=f"{data['time']}").grid(
                row=row, column=1, padx=5, pady=2)
            ttk.Label(table_frame, text=f"{data['exp']:.1f}").grid(
                row=row, column=2, padx=5, pady=2)
    
    def show_stats_graphs(self, stats):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
        
        subjects = list(stats.keys())
        times = [stats[s]['time'] for s in subjects]
        exps = [stats[s]['exp'] for s in subjects]
        colors = [SUBJECTS[s]['color'] for s in subjects]
        labels = [SUBJECTS[s]['name_en'] for s in subjects]
        
        # 学習時間グラフ
        ax1.bar(labels, times, color=colors)
        ax1.set_title('Study Time by Subject')
        ax1.set_ylabel('Time (minutes)')
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        
        # EXPグラフ
        ax2.bar(labels, exps, color=colors)
        ax2.set_title('EXP Gained by Subject')
        ax2.set_ylabel('EXP')
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.parent)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)