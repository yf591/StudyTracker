import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import AutoDateLocator, DateFormatter, DayLocator, WeekdayLocator, MonthLocator
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from utils.analytics import (
    prepare_study_data,
    create_prediction_model,
    predict_achievement_dates,
    predict_total_achievement,
    predict_subject_achievement
)
from utils.config import SUBJECTS

class AnalysisView:
    TAB_NAME = "分析データ"

    def __init__(self, parent, tracker):
        """初期化"""
        self.parent = parent
        self.tracker = tracker
        self.setup_view()

    def setup_view(self):
        # サブタブのメインフレーム
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(expand=True, fill='both')

        # サブタブ用のNotebook
        self.sub_notebook = ttk.Notebook(self.main_frame)
        self.sub_notebook.pack(expand=True, fill='both')

        # 各サブタブのフレーム作成
        self.progress_frame = ttk.Frame(self.sub_notebook)
        self.time_frame = ttk.Frame(self.sub_notebook)
        self.prediction_frame = ttk.Frame(self.sub_notebook)

        # サブタブの追加
        self.sub_notebook.add(self.progress_frame, text='Learning Progress')
        self.sub_notebook.add(self.time_frame, text='Time Analysis')
        self.sub_notebook.add(self.prediction_frame, text='Time Prediction')

        # 各サブタブの内容を作成
        self.create_progress_graph(self.progress_frame)
        self.create_time_analysis(self.time_frame)
        self.create_time_prediction(self.prediction_frame)

    def create_progress_graph(self, frame):
        if not self.tracker.study_log:
            ttk.Label(frame, text="データがありません").pack(pady=10)
            return

        # データフレームの作成
        df = pd.DataFrame([
            {
                'date': datetime.strptime(log[4], '%Y-%m-%d %H:%M'),
                'exp': log[3]
            } for log in self.tracker.study_log
        ])

        # 日付インデックスの設定
        df.set_index('date', inplace=True)
        df.sort_index(inplace=True)

        # 日次・週次・月次データの準備
        daily_data = df.resample('D')['exp'].sum()
        weekly_data = df.resample('W')['exp'].sum()
        monthly_data = df.resample('M')['exp'].sum()

        fig = plt.figure(figsize=(12, 10), dpi=100)  # DPIを上げて解像度を向上
        gs = fig.add_gridspec(3, 1, hspace=0.4)

        # グラフのスタイル設定 (共通)
        bar_width = 0.7  # 棒の幅
        edgecolor = 'black'  # 棒の枠線の色
        linewidth = 0.5      # 枠線の太さ

        # 日次グラフ (直近7日)
        ax1 = fig.add_subplot(gs[0])
        if len(daily_data) > 0:
            start_date = daily_data.index[-1] - timedelta(days=6)
            ax1.bar(daily_data.index[-7:], daily_data.values[-7:],  # barに変更
                    color='#e74c3c',  # より鮮やかな赤色
                    width=bar_width, edgecolor=edgecolor, linewidth=linewidth,
                    label='Daily EXP')
            ax1.set_xlim(start_date, daily_data.index[-1])
            ax1.xaxis.set_major_locator(DayLocator())
            ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

        ax1.set_title('Daily EXP Progress (Last 7 Days)', pad=15, fontweight='bold') # タイトルを太字に
        ax1.set_xlabel('Date', fontweight='bold')
        ax1.set_ylabel('EXP Gained', fontweight='bold')
        plt.setp(ax1.get_xticklabels(), rotation=45)
        ax1.grid(True, alpha=0.3, linestyle='--')  # グリッドを点線に
        ax1.legend()

        # 週次グラフ (直近8週)
        ax2 = fig.add_subplot(gs[1])
        if len(weekly_data) > 0:
            start_date = weekly_data.index[-1] - timedelta(weeks=7)
            ax2.bar(weekly_data.index[-8:], weekly_data.values[-8:],  # barに変更
                    color='#2ecc71',  # より鮮やかな緑色
                    width=bar_width, edgecolor=edgecolor, linewidth=linewidth,
                    label='Weekly EXP')
            ax2.set_xlim(start_date, weekly_data.index[-1])
            ax2.xaxis.set_major_locator(WeekdayLocator(byweekday=0))
            ax2.xaxis.set_major_formatter(DateFormatter('%Y-W%U'))

        ax2.set_title('Weekly EXP Progress (Last 8 Weeks)', pad=15, fontweight='bold')
        ax2.set_xlabel('Week', fontweight='bold')
        ax2.set_ylabel('EXP Gained', fontweight='bold')
        plt.setp(ax2.get_xticklabels(), rotation=45)
        ax2.grid(True, alpha=0.3, linestyle='--')
        ax2.legend()


        # 月次グラフ (直近12か月)
        ax3 = fig.add_subplot(gs[2])
        if len(monthly_data) > 0:
            start_date = monthly_data.index[-1] - pd.DateOffset(months=11)
            ax3.bar(monthly_data.index[-12:], monthly_data.values[-12:],  # barに変更
                    color='#3498db', # より鮮やかな青色
                    width=bar_width*1.2, edgecolor=edgecolor, linewidth=linewidth,  # 月次グラフは棒を少し太く
                    label='Monthly EXP')
            ax3.set_xlim(start_date, monthly_data.index[-1])
            ax3.xaxis.set_major_locator(MonthLocator())
            ax3.xaxis.set_major_formatter(DateFormatter('%Y-%m'))

        ax3.set_title('Monthly EXP Progress (Last 12 Months)', pad=15, fontweight='bold')
        ax3.set_xlabel('Month', fontweight='bold')
        ax3.set_ylabel('EXP Gained', fontweight='bold')
        plt.setp(ax3.get_xticklabels(), rotation=45)
        ax3.grid(True, alpha=0.3, linestyle='--')
        ax3.legend()

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

        # 説明ボタン
        ttk.Button(frame, text="グラフの説明",
                  command=self.show_progress_explanation).pack(pady=5)

    def show_progress_explanation(self):
        messagebox.showinfo("グラフの説明",
            "【Learning Progress Graphs】\n\n"
            "日次グラフ（赤）:\n"
            "- 日ごとの獲得EXPを表示\n"
            "- 日々の学習成果を詳細に確認できます\n\n"
            "週次グラフ（緑）:\n"
            "- 週ごとの獲得EXPの合計を表示\n"
            "- 週単位での学習の傾向を把握できます\n\n"
            "月次グラフ（青）:\n"
            "- 月ごとの獲得EXPの合計を表示\n"
            "- 月単位での学習の進捗を確認できます")

    def create_time_analysis(self, frame):
        if not self.tracker.study_log:
            ttk.Label(frame, text="No data available").pack(pady=10)
            return

        fig = plt.figure(figsize=(12, 8))
        gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.2])

        # 時間帯別学習時間（グラデーションカラー）
        ax1 = fig.add_subplot(gs[0, 0])
        self.plot_hourly_distribution(ax1)

        # 曜日別学習時間（虹色パレット）
        ax2 = fig.add_subplot(gs[0, 1])
        self.plot_weekday_distribution(ax2)

        # 学習時間推移（2色グラデーション）
        ax3 = fig.add_subplot(gs[1, :])
        self.plot_study_time_trend(ax3)

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

        # 説明ボタンの追加
        ttk.Button(frame, text="グラフの説明",
                  command=self.show_time_analysis_explanation).pack(pady=5)

    def plot_hourly_distribution(self, ax):
        hours = [datetime.strptime(log[4], '%Y-%m-%d %H:%M').hour
                 for log in self.tracker.study_log]
        minutes = [log[1] for log in self.tracker.study_log]

        hour_stats = {h: 0 for h in range(24)}
        for h, m in zip(hours, minutes):
            hour_stats[h] += m

        colors = plt.cm.viridis(np.linspace(0, 1, 24))
        ax.bar(hour_stats.keys(), hour_stats.values(), color=colors)
        ax.set_title('Study Time by Hour', fontsize=12, pad=10)
        ax.set_xlabel('Hour of Day')
        ax.set_ylabel('Total Minutes')

    def plot_weekday_distribution(self, ax):
        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        dates = [datetime.strptime(log[4], '%Y-%m-%d %H:%M')
                 for log in self.tracker.study_log]
        minutes = [log[1] for log in self.tracker.study_log]

        weekday_stats = {i: 0 for i in range(7)}
        for d, m in zip(dates, minutes):
            weekday_stats[d.weekday()] += m

        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99',
                 '#ff99cc', '#99ffcc', '#ff99ff']
        ax.bar(weekdays, [weekday_stats[i] for i in range(7)], color=colors)
        ax.set_title('Study Time by Weekday', fontsize=12, pad=10)
        ax.set_xlabel('Weekday')
        ax.set_ylabel('Total Minutes')

    def plot_study_time_trend(self, ax):
        dates = [datetime.strptime(log[4], '%Y-%m-%d %H:%M')
                 for log in self.tracker.study_log]
        minutes = [log[1] for log in self.tracker.study_log]

        colors = np.zeros((len(dates), 4))
        colors[:, 0] = np.linspace(0.2, 0.8, len(dates))  # Red channel
        colors[:, 2] = np.linspace(0.8, 0.2, len(dates))  # Blue channel
        colors[:, 3] = 1  # Alpha channel

        ax.scatter(dates, minutes, c=colors)
        ax.plot(dates, minutes, color='#2c3e50', alpha=0.5)
        ax.set_title('Study Time Trend', fontsize=12, pad=10)
        ax.set_xlabel('Date')
        ax.set_ylabel('Minutes per Session')
        plt.setp(ax.get_xticklabels(), rotation=45)


    def show_time_analysis_explanation(self):
        messagebox.showinfo("グラフの説明",
            "【Time Analysis Graphs】\n\n"
            "時間帯別学習時間（グラデーション）:\n"
            "- 24時間の各時間帯における総学習時間を表示\n"
            "- 最も集中して学習できる時間帯を把握できます\n\n"
            "曜日別学習時間（レインボー）:\n"
            "- 曜日ごとの総学習時間を表示\n"
            "- 学習パターンの週間リズムを確認できます\n\n"
            "学習時間推移（グラデーション）:\n"
            "- 日付順の学習時間の変化を表示\n"
            "- 学習時間の増減傾向を可視化します")

    def create_time_prediction(self, frame):
        if len(self.tracker.study_log) < 5:
            ttk.Label(frame, text="予測するには最低5件の学習記録が必要です").pack(pady=10)
            return

        # 目標時間の設定
        target_hours = [10, 20, 30, 40, 50, 100, 200, 300, 400, 500,
                       1000, 2000, 3000, 4000, 5000, 10000]

        # モデルの説明
        model_desc = (
            "【予測モデル情報】\n"
            "手法: 直近7日間の平均学習時間に基づく線形予測\n"
            "特徴: 最新の学習ペースを重視した予測\n"
            "注意: 予測値は現在の学習ペースが継続すると仮定した場合の参考値です\n\n"
        )

        result_frame = ttk.LabelFrame(frame, text="目標達成予測")
        result_frame.pack(pady=10, padx=10, fill='both', expand=True)

        text_widget = tk.Text(result_frame, height=40, width=70, font=('Helvetica', 10))
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical",
                                command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # モデル説明の追加
        text_widget.insert(tk.END, model_desc)

        # 全体の予測
        text_widget.insert(tk.END, "【全データ】\n")
        total_predictions = predict_total_achievement(self.tracker.study_log, target_hours)
        for target, days in total_predictions:
            years, months, remain_days = self.convert_days(days)
            text_widget.insert(tk.END,
                f"{target}時間到達まで: 約{days}日 （{years}年{months}か月{remain_days}日）\n")

        # 科目別の予測
        for subject in SUBJECTS.keys():
            text_widget.insert(tk.END, f"\n【{subject}】\n")
            subject_predictions = predict_subject_achievement(
                self.tracker.study_log, subject, target_hours)
            for target, days in subject_predictions:
                years, months, remain_days = self.convert_days(days)
                text_widget.insert(tk.END,
                    f"{target}時間到達まで: 約{days}日 （{years}年{months}か月{remain_days}日）\n")

        text_widget.configure(state='disabled')

    def convert_days(self, total_days):
        years = total_days // 365
        remaining_days = total_days % 365
        months = remaining_days // 30
        days = remaining_days % 30
        return int(years), int(months), int(days)