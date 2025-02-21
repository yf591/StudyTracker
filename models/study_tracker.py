import json
import os
from datetime import datetime

class StudyTracker:
    def __init__(self):
        self.data_file = "study_data.json"
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.exp = data.get('exp', 0)
                self.level = data.get('level', 1)
                self.tickets = data.get('tickets', 0)
                self.study_log = data.get('study_log', [])
        else:
            self.exp = 0
            self.level = 1
            self.tickets = 0
            self.study_log = []

    def save_data(self):
        data = {
            'exp': self.exp,
            'level': self.level,
            'tickets': self.tickets,
            'study_log': self.study_log
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f)

    def add_study(self, minutes, subject, difficulty):
        earned_exp = minutes * difficulty
        self.exp += earned_exp
        study_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.study_log.append((len(self.study_log) + 1, minutes, subject, earned_exp, study_date))
        self.check_level_up()
        self.save_data()
        return earned_exp

    def check_level_up(self, skip_save=False):
        required_exp = 100 * (self.level ** 1.5)
        while self.exp >= required_exp:
            self.level += 1
            self.tickets += 1
            self.exp -= required_exp
            required_exp = 100 * (self.level ** 1.5)
        if not skip_save:
            self.save_data()

    def use_ticket(self):
        if self.tickets > 0:
            self.tickets -= 1
            self.save_data()
            return True
        return False

    def reset_day(self, target_date):
        self.study_log = [log for log in self.study_log if log[4].split()[0] != target_date]
        self.recalculate_stats()

    def modify_record(self, record_id, minutes, subject, difficulty):
        for i, log in enumerate(self.study_log):
            if log[0] == record_id:
                new_exp = minutes * difficulty
                self.study_log[i] = (record_id, minutes, subject, new_exp, log[4])
                break
        self.recalculate_stats()

    def recalculate_stats(self):
        self.exp = 0
        self.level = 1
        self.tickets = 0
        sorted_log = sorted(self.study_log, key=lambda x: x[4])
        for log in sorted_log:
            self.exp += log[3]
            self.check_level_up(skip_save=True)
        self.save_data()

    def reset_all(self):
        """全データをリセット"""
        self.exp = 0
        self.level = 1
        self.tickets = 0
        self.study_log = []
        self.save_data()
        return True