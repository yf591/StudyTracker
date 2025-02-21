import tkinter as tk
from tkinter import ttk
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from models.study_tracker import StudyTracker
from utils.config import APP_CONFIG, SUBJECTS
from .dialogs import RecordEditDialog
from .stats.status_view import StatusView
from .stats.subject_view import SubjectView
from .stats.daily_view import DailyView
from .stats.management_view import ManagementView
from .stats.analysis_view import AnalysisView

class StudyApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_CONFIG["title"])
        self.root.geometry(APP_CONFIG["window_size"])
        self.tracker = StudyTracker()
        
        self.setup_main_interface()
        self.setup_stats_window()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_main_interface(self):
        # スタイル設定
        style = ttk.Style()
        style.configure('Large.TMenubutton', font=('Helvetica', 14))  # 1.5倍
        style.configure('Timer.TLabel', font=('Helvetica', 24))       # 2倍
        style.configure('Button.TButton', font=('Helvetica', 12))

        # タイトル
        self.label = ttk.Label(self.root, text="勉強してレベルアップしよう！")
        self.label.pack(pady=10)

        # 科目選択（1.5倍）
        self.subject_var = tk.StringVar(value=list(SUBJECTS.keys())[0])
        self.subject_menu = ttk.OptionMenu(
            self.root, 
            self.subject_var, 
            list(SUBJECTS.keys())[0], 
            *SUBJECTS.keys(),
            style='Large.TMenubutton'
        )
        self.subject_menu.pack(pady=10)

        # タイマー機能（2倍）
        self.setup_timer()

        # 勉強時間入力と記録ボタンを横に並べるフレーム
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=5)
        
        # 勉強時間入力（1.5倍）
        self.minutes_var = tk.IntVar(value=30)
        self.minutes_entry = ttk.Entry(
            input_frame, 
            textvariable=self.minutes_var,
            font=('Helvetica', 14)  # 1.5倍のフォントサイズ
        )
        self.minutes_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(input_frame, text="勉強時間（分）").pack(side=tk.LEFT, padx=5)
        
        # 記録ボタンを入力欄の横に配置
        ttk.Button(input_frame, text="勉強を記録", 
                  command=self.add_study,
                  style='Button.TButton').pack(side=tk.LEFT, padx=5)

        # ボタンフレーム（チケットとステータス確認のみ）
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=5)
        
        for btn in ["チケットを使う", "ステータスの確認"]:
            ttk.Button(button_frame, text=btn, 
                      command=self.get_button_command(btn),
                      style='Button.TButton').pack(side=tk.LEFT, padx=5)

        # ステータステキスト（縦2倍）
        self.status_text = tk.Text(self.root, height=20, width=70)  # heightを2倍に
        self.status_text.pack(pady=10)

    def setup_timer(self):
        self.timer_running = False
        self.paused = False
        self.start_time = 0
        self.pause_time = 0
        self.timer_id = None
        
        self.timer_label = ttk.Label(self.root, text="00:00:00", style='Timer.TLabel')
        self.timer_label.pack(pady=5)
        
        timer_frame = ttk.Frame(self.root)
        timer_frame.pack(pady=5)
        
        # タイマーボタン
        timer_buttons = [
            ("開始", self.start_timer),
            ("一時停止", self.pause_timer),
            ("終了", self.stop_timer),
            ("リセット", self.reset_timer)
        ]
        
        for text, command in timer_buttons:
            btn = ttk.Button(timer_frame, text=text, command=command, style='Button.TButton')
            btn.pack(side=tk.LEFT, padx=5)
            if text == "一時停止":
                self.pause_button = btn
            elif text == "開始":
                self.start_button = btn
        
        self.update_timer_buttons("ready")

    def update_timer_buttons(self, state):
        if state == "ready":
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
        elif state == "running":
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
        elif state == "paused":
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.NORMAL)

    def start_timer(self):
        """タイマー開始機能の修正"""
        if self.paused:
            self.start_time = time.time() - (self.pause_time - self.start_time)
        else:
            self.start_time = time.time()
        
        self.timer_running = True
        self.paused = False
        self.update_timer_buttons("running")
        self.update_timer()  # タイマー更新を即座に開始

    def pause_timer(self):
        if self.timer_running:
            self.pause_time = time.time()
            self.paused = True
            self.timer_running = False
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            self.update_timer_buttons("paused")

    def stop_timer(self):
        if self.timer_running or self.paused:
            self.timer_running = False
            self.paused = False
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            elapsed_minutes = int((time.time() - self.start_time) / 60)
            self.minutes_var.set(elapsed_minutes)
            self.update_timer_buttons("ready")

    def reset_timer(self):
        self.timer_running = False
        self.paused = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.timer_label.config(text="00:00:00")
        self.update_timer_buttons("ready")

    def get_button_command(self, btn_text):
        if btn_text == "チケットを使う":
            return self.confirm_use_ticket
        elif btn_text == "勉強を記録":
            return self.add_study
        else:
            return self.show_stats

    def confirm_use_ticket(self):
        if tk.messagebox.askyesno("確認", "チケットを使用しますか？"):
            if self.tracker.use_ticket():
                self.status_text.insert(tk.END, 
                    f"チケットを使ったよ！楽しんでね！（残り: {self.tracker.tickets}）\n")
            else:
                self.status_text.insert(tk.END, 
                    "チケットが足りないよ！もっと勉強して稼ごう！\n")

    def setup_stats_window(self):
        """統計ウィンドウの設定"""
        self.stats_views = [
            ('status', StatusView, "現在のステータス"),
            ('subject', SubjectView, "科目別統計"),
            ('daily', DailyView, "日別統計"),
            ('management', ManagementView, "記録管理"),
            ('analysis', AnalysisView, "分析データ")
        ]

    def show_stats(self):
        """統計ウィンドウの表示"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("ステータスの確認")
        stats_window.geometry("900x800")

        notebook = ttk.Notebook(stats_window)
        notebook.pack(expand=True, fill='both', padx=5, pady=5)

        # 各タブの作成
        for view_id, view_class, tab_name in self.stats_views:
            frame = ttk.Frame(notebook)
            frame.pack(expand=True, fill='both')
            view = view_class(frame, self.tracker)
            notebook.add(frame, text=tab_name)

        # ウィンドウの設定
        stats_window.transient(self.root)
        stats_window.grab_set()

    def on_closing(self):
        if self.timer_running:
            self.stop_timer()
        self.tracker.save_data()
        self.root.destroy()

    # タイマー関連のメソッド
    def update_timer(self):
        """タイマー更新機能の修正"""
        if self.timer_running:
            current_time = time.time()
            elapsed_time = int(current_time - self.start_time)
            hours = elapsed_time // 3600
            minutes = (elapsed_time % 3600) // 60
            seconds = elapsed_time % 60
            self.timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.timer_id = self.root.after(1000, self.update_timer)

    # 勉強記録関連のメソッド
    def add_study(self):
        minutes = self.minutes_var.get()
        subject = self.subject_var.get()
        difficulty = SUBJECTS[subject]["difficulty"]
        earned_exp = self.tracker.add_study(minutes, subject, difficulty)
        
        self.status_text.insert(tk.END, 
            f"{subject}を{minutes}分勉強！ EXP +{earned_exp:.1f}\n"
            f"現在のレベル: {self.tracker.level}, "
            f"EXP: {self.tracker.exp:.1f}, "
            f"チケット: {self.tracker.tickets}\n"
        )

    def use_ticket(self):
        if self.tracker.use_ticket():
            self.status_text.insert(tk.END, 
                f"チケットを使ったよ！楽しんでね！（残り: {self.tracker.tickets}）\n"
            )
        else:
            self.status_text.insert(tk.END, 
                "チケットが足りないよ！もっと勉強して稼ごう！\n"
            )