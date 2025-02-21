import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from ..dialogs import RecordEditDialog

class ManagementView:
    TAB_NAME = "記録管理"
    
    def __init__(self, parent, tracker):
        self.parent = parent
        self.tracker = tracker
        self.setup_view()
    
    def setup_view(self):
        # 全記録リセット
        ttk.Button(self.parent, text="全記録をリセット", 
                  command=self.confirm_reset_all).pack(pady=5)
        
        # 日付指定リセット
        cal_frame = ttk.LabelFrame(self.parent, text="日付指定リセット")
        cal_frame.pack(pady=5, padx=5, fill="x")
        
        self.cal = Calendar(cal_frame, selectmode='day', 
                          date_pattern='y-mm-dd')
        self.cal.pack(pady=5)
        
        ttk.Button(cal_frame, text="指定日をリセット", 
                  command=self.reset_selected_day).pack(pady=5)
        
        # 記録修正/削除
        edit_frame = ttk.LabelFrame(self.parent, text="記録の修正/削除")
        edit_frame.pack(pady=10, padx=5, fill="x")
        
        self.edit_id_var = tk.IntVar()
        ttk.Label(edit_frame, text="記録ID:").pack(pady=5)
        ttk.Entry(edit_frame, textvariable=self.edit_id_var).pack(pady=5)
        
        button_frame = ttk.Frame(edit_frame)
        button_frame.pack(pady=5)
        
        ttk.Button(button_frame, text="記録を修正", 
                  command=self.edit_record).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="記録を削除", 
                  command=self.delete_record).pack(side=tk.LEFT, padx=5)
    
    def confirm_reset_all(self):
        if messagebox.askyesno("確認", "全ての記録をリセットしますか？"):
            self.tracker.reset_all()
            messagebox.showinfo("完了", "全ての記録をリセットしました")
    
    def reset_selected_day(self):
        selected_date = self.cal.get_date()
        if messagebox.askyesno("確認", 
                             f"{selected_date}の記録をリセットしますか？"):
            self.tracker.reset_day(selected_date)
            messagebox.showinfo("完了", "指定日の記録をリセットしました")
    
    def edit_record(self):
        record_id = self.edit_id_var.get()
        dialog = RecordEditDialog(self.parent, self.tracker, record_id)
    
    def delete_record(self):
        record_id = self.edit_id_var.get()
        if messagebox.askyesno("確認", f"記録 #{record_id} を削除しますか？"):
            self.tracker.delete_record(record_id)
            messagebox.showinfo("完了", "記録を削除しました")