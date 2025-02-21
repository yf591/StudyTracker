import tkinter as tk
from views.app import StudyApp
import sys

def check_requirements():
    try:
        import matplotlib
        import pandas
        import numpy
        return True
    except ImportError as e:
        tk.messagebox.showerror(
            "エラー",
            "必要なパッケージが不足しています。\n"
            "以下のコマンドを実行してください：\n"
            "pip install matplotlib pandas numpy"
        )
        return False

if __name__ == "__main__":
    if check_requirements():
        root = tk.Tk()
        app = StudyApp(root)
        root.mainloop()