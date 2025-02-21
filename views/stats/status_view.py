import tkinter as tk
from tkinter import ttk

class StatusView:
    TAB_NAME = "現在のステータス"
    
    def __init__(self, parent, tracker):
        self.parent = parent
        self.tracker = tracker
        self.setup_view()
    
    def setup_view(self):
        # フォントサイズを大きくする
        large_font = ('Helvetica', 16)  # 16ポイントに設定
        
        # 総計の計算
        total_exp = sum(log[3] for log in self.tracker.study_log)
        total_time = sum(log[1] for log in self.tracker.study_log)
        next_level_exp = 100 * (self.tracker.level ** 1.5)
        exp_needed = next_level_exp - self.tracker.exp
        
        # ステータス情報（フォントサイズを大きく）
        info_texts = [
            f"総獲得経験値: {total_exp:.1f} EXP",
            f"総学習時間: {total_time} 分",
            f"現在のレベル: {self.tracker.level}",
            f"次のレベルまでに必要な経験値: {exp_needed:.1f} EXP",
            f"残チケット数: {self.tracker.tickets}枚"
        ]
        
        for text in info_texts:
            ttk.Label(
                self.parent, 
                text=text,
                font=large_font
            ).pack(pady=10)