import tkinter as tk
from tkinter import ttk, messagebox
from utils.config import SUBJECTS

class RecordEditDialog(tk.Toplevel):
    def __init__(self, parent, tracker, record_id):
        super().__init__(parent)
        self.title("記録の修正")
        self.tracker = tracker
        self.record_id = record_id
        self.result = False
        
        # 現在の記録を取得
        self.record = next(
            (log for log in tracker.study_log if log[0] == record_id), 
            None
        )
        
        if self.record is None:
            messagebox.showerror("エラー", "指定されたIDの記録が見つかりません")
            self.destroy()
            return
            
        self.setup_dialog()

    def setup_dialog(self):
        # 現在の値を表示
        ttk.Label(self, text=f"記録 #{self.record[0]}").pack(pady=5)
        ttk.Label(self, text=f"日時: {self.record[4]}").pack(pady=5)
        
        # 学習時間入力
        self.minutes_var = tk.IntVar(value=self.record[1])
        ttk.Label(self, text="学習時間（分）:").pack(pady=5)
        ttk.Entry(self, textvariable=self.minutes_var).pack()
        
        # 科目選択
        self.subject_var = tk.StringVar(value=self.record[2])
        ttk.Label(self, text="科目:").pack(pady=5)
        ttk.OptionMenu(self, self.subject_var, self.record[2], *SUBJECTS.keys()).pack()
        
        # 保存ボタン
        ttk.Button(self, text="保存", command=self.save_changes).pack(pady=10)

    def save_changes(self):
        if messagebox.askyesno("確認", "この変更を保存してもよろしいですか？"):
            minutes = self.minutes_var.get()
            subject = self.subject_var.get()
            difficulty = SUBJECTS[subject]["difficulty"]
            
            self.tracker.modify_record(self.record_id, minutes, subject, difficulty)
            self.result = True
            self.destroy()
            messagebox.showinfo("完了", "記録を修正しました")