import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime
import numpy as np

def prepare_study_data(study_log):
    """学習データの準備"""
    if not study_log:
        return None
    
    df = pd.DataFrame([
        {
            'date': datetime.strptime(log[4], '%Y-%m-%d %H:%M'),
            'minutes': log[1],
            'subject': log[2],
            'exp': log[3]
        }
        for log in study_log
    ])
    
    df['days_from_start'] = (df['date'] - df['date'].min()).dt.days
    df['weekday'] = df['date'].dt.weekday
    df['hour'] = df['date'].dt.hour
    
    return df

def create_prediction_model(df):
    """予測モデルの作成"""
    if df is None or len(df) < 5:
        return None, "予測するには最低5件の学習記録が必要です"

    # 特徴量の準備
    df_encoded = pd.get_dummies(df, columns=['subject'])
    features = ['days_from_start', 'weekday', 'hour'] + [col for col in df_encoded.columns if col.startswith('subject_')]
    
    X = df_encoded[features]
    y = df_encoded['minutes']
    
    model = LinearRegression()
    model.fit(X, y)
    
    return model, None

def predict_achievement_dates(model, current_data, target_hours):
    """目標達成日の予測"""
    if model is None:
        return []
        
    df = prepare_study_data(current_data)
    if df is None:
        return []
        
    current_total = df['minutes'].sum() / 60  # 現在の総学習時間（時間）
    predictions = []
    
    for target in target_hours:
        if current_total < target:
            remaining_hours = target - current_total
            # 直近の学習ペースから予測
            recent_pace = df.tail(min(len(df), 7))['minutes'].mean() / 60  # 時間/日
            if recent_pace > 0:
                days_needed = remaining_hours / recent_pace
                predictions.append((target, max(1, int(days_needed))))
    
    return predictions

def predict_total_achievement(study_log, target_hours):
    """全体の学習時間予測"""
    if len(study_log) < 5:
        return []
    
    df = prepare_study_data(study_log)
    if df is None:
        return []
    
    current_total = df['minutes'].sum() / 60  # 現在の総学習時間（時間）
    predictions = []
    
    # 直近7日間の平均学習時間を計算
    recent_data = df.tail(min(len(df), 7))
    daily_average = recent_data['minutes'].mean() / 60  # 1日あたりの平均学習時間（時間）
    
    for target in target_hours:
        if current_total < target:
            remaining_hours = target - current_total
            days_needed = int(remaining_hours / daily_average) if daily_average > 0 else 999999
            predictions.append((target, max(1, days_needed)))
    
    return predictions

def predict_subject_achievement(study_log, subject, target_hours):
    """科目ごとの学習時間予測"""
    if len(study_log) < 5:
        return []
    
    df = prepare_study_data(study_log)
    if df is None:
        return []
    
    # 特定の科目のデータのみ抽出
    subject_df = df[df['subject'] == subject]
    if len(subject_df) == 0:
        return [(h, 999999) for h in target_hours]  # データがない場合は最大値
    
    current_total = subject_df['minutes'].sum() / 60
    predictions = []
    
    # 直近のデータから1日あたりの平均学習時間を計算
    recent_data = subject_df.tail(min(len(subject_df), 7))
    daily_average = recent_data['minutes'].mean() / 60
    
    for target in target_hours:
        if current_total < target:
            remaining_hours = target - current_total
            days_needed = int(remaining_hours / daily_average) if daily_average > 0 else 999999
            predictions.append((target, max(1, days_needed)))
    
    return predictions