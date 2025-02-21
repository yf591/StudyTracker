# 科目設定
SUBJECTS = {
    "Mathematics": {"name_en": "Mathematics", "color": "blue", "difficulty": 1.0},
    "English": {"name_en": "English", "color": "yellow", "difficulty": 1.0},
    "プログラミング": {"name_en": "Programming", "color": "green", "difficulty": 1.2},
    "機械学習（深層・強化・LLMなど）": {"name_en": "Machine Learning", "color": "red", "difficulty": 1.5}
}

# グラフ設定
GRAPH_DEFAULTS = {
    "figsize": (8, 4),
    "rotation": 45,
    "padding": 10
}

# アプリケーション設定
APP_CONFIG = {
    "window_size": "800x900",
    "title": "Study Level-up System"
}

# タイマー設定
TIMER_CONFIG = {
    "update_interval": 1000,  # ミリ秒
    "format": "%H:%M:%S"
}