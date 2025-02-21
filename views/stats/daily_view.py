import tkinter as tk
from tkinter import ttk
from datetime import datetime

class DailyView:
    TAB_NAME = "日別統計"
    
    def __init__(self, parent, tracker):
        self.parent = parent
        self.tracker = tracker
        self.setup_view()
    
    def setup_view(self):
        # スクロール可能なテキストウィジェット
        self.text_widget = tk.Text(self.parent, height=20, width=50)
        scrollbar = ttk.Scrollbar(self.parent, orient="vertical", 
                                command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        self.text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.show_daily_stats()
    
    def show_daily_stats(self):
        self.text_widget.insert(tk.END, "学習記録:\n\n")
        
        # 日付の新しい順にソート
        sorted_logs = sorted(
            self.tracker.study_log,
            key=lambda x: (
                datetime.strptime(x[4], '%Y-%m-%d %H:%M'),
                -x[0]  # 同じ日時の場合はIDの大きい順
            ),
            reverse=True
        )
        
        for log in sorted_logs:
            record_id, minutes, subject, exp, date = log
            self.text_widget.insert(tk.END, (
                f"記録 #{record_id}\n"
                f"日時: {date}\n"
                f"科目: {subject}\n"
                f"時間: {minutes}分\n"
                f"獲得EXP: {exp:.1f}\n"
                f"------------------------\n"
            ))
        
        self.text_widget.configure(state='disabled')