# StudyTracker

学習時間を経験値とレベルに変換してゲーム感覚で管理できる学習管理アプリケーションです。

## 特徴

- 📊 科目別の学習時間と進捗の記録
- 🎮 経験値とレベルによるゲーミフィケーション
- 📈 詳細な分析とデータの可視化
- 🎯 日次/週次/月次の進捗確認
- 🎫 モチベーション維持のための報酬チケットシステム
- 📝 学習記録の管理機能


## リポジトリ構成
```bash
StudyTracker/
├── main.py              # アプリケーションのエントリーポイント
├── models/              # データモデルを格納するディレクトリ
│   ├── __init__.py     # Pythonパッケージ化のための初期化ファイル
│   └── study_tracker.py # 学習データの管理と保存を行うモデルクラス
├── views/               # GUIコンポーネントを格納するディレクトリ
│   ├── __init__.py     # Pythonパッケージ化のための初期化ファイル
│   ├── app.py          # メインアプリケーションのGUIクラス
│   ├── dialogs.py      # ダイアログウィンドウのクラス群
│   └── stats/          # 統計情報表示用のビューを格納するディレクトリ
│       ├── __init__.py # Pythonパッケージ化のための初期化ファイル
│       ├── analysis_view.py  # 分析データ表示用のビュークラス
│       ├── daily_view.py     # 日別統計表示用のビュークラス
│       ├── management_view.py # 記録管理用のビュークラス
│       └── status_view.py    # 現在のステータス表示用のビュークラス
└── utils/              # ユーティリティ機能を格納するディレクトリ
    ├── __init__.py    # Pythonパッケージ化のための初期化ファイル
    ├── analytics.py   # データ分析用のユーティリティ関数
    └── config.py      # アプリケーション設定の定義
```

## はじめ方

1. リポジトリのクローン
```bash
git clone https://github.com/yourusername/StudyTracker.git
cd StudyTracker
```

2. リポジトリのクローン
```bash
pip install matplotlib pandas numpy tkinter
```

3. リポジトリのクローン
```bash
python main.py
```

## 免責事項
本アプリケーションは現状のまま提供され、いかなる保証もありません。使用は自己責任でお願いします。

## ライセンス
このプロジェクトはMITライセンスの下で提供されています - 詳細はLICENSEファイルを参照してください。