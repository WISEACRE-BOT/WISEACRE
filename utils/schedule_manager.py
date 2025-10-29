import json
import os
from datetime import datetime, date, timedelta, timezone
from typing import List, Dict

MOSCOW_TZ = timezone(timedelta(hours=3))


class ScheduleManager:
    def __init__(self, schedule_file: str = "data/schedule.json"):
        self.schedule_file = schedule_file
        self.schedule_data = self._load_schedule()
        self.start_date = datetime.strptime(
            self.schedule_data.get("start_date", "2025-09-01"), "%Y-%m-%d"
        ).date()

    def _load_schedule(self) -> Dict:
        if not os.path.exists(self.schedule_file):
            raise FileNotFoundError(f"Файл {self.schedule_file} не найден.")
        with open(self.schedule_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_week_type(self, target_date: date = None) -> str:
        if target_date is None:
            target_date = datetime.now(MOSCOW_TZ).date()
        delta_days = (target_date - self.start_date).days
        week_num = (delta_days // 7) + 1
        return "odd" if week_num % 2 == 1 else "even"

    def get_day_schedule(self, target_date: date) -> List[Dict]:
        date_str = target_date.strftime("%Y-%m-%d")
        if date_str in self.schedule_data.get("special_dates", {}):
            return self.schedule_data["special_dates"][date_str]
        day_name = target_date.strftime("%A").lower()
        week_type = self.get_week_type(target_date)
        return self.schedule_data.get(f"{week_type}_week", {}).get(day_name, [])

    def get_schedule_for_date(self, date_str: str) -> str:
        try:
            target_date = datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError:
            return "⚠️ Неверный формат даты. Используй формат: 31.10.2025"
        schedule = self.get_day_schedule(target_date)
        return self.format_schedule(schedule, target_date)

    def get_today_schedule(self) -> str:
        today = datetime.now(MOSCOW_TZ).date()
        schedule = self.get_day_schedule(today)
        return self.format_schedule(schedule, today)

    def get_tomorrow_schedule(self) -> str:
        tomorrow = (datetime.now(MOSCOW_TZ) + timedelta(days=1)).date()
        schedule = self.get_day_schedule(tomorrow)
        return self.format_schedule(schedule, tomorrow)

    def get_week_schedule(self) -> Dict[str, List[Dict]]:
        week_schedule = {}
        today = datetime.now(MOSCOW_TZ).date()
        start_of_week = today - timedelta(days=today.weekday())
        days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
        for i, day in enumerate(days):
            current_day = start_of_week + timedelta(days=i)
            schedule = self.get_day_schedule(current_day)
            if schedule:
                week_schedule[day] = schedule
        return week_schedule

    def format_schedule(self, schedule: List[Dict], target_date: date) -> str:
        date_str = target_date.strftime("%d.%m.%Y (%A)")
        week_type_text = "нечётная" if self.get_week_type(target_date) == "odd" else "чётная"
        if not schedule:
            return f"📅 {date_str}\nПар нет 🎉\n({week_type_text} неделя)"
        msg = f"📅 Расписание на {date_str}\n🗓 {week_type_text} неделя\n\n"
        for i, pair in enumerate(schedule, 1):
            msg += (
                f"🕒 {pair['time']}\n"
                f"📘 {pair['subject']}\n"
                f"🎓 {pair['type']}\n"
                f"🏫 {pair['room']}\n"
                f"👨‍🏫 {pair['teacher']}\n"
            )
            if i < len(schedule):
                msg += "━━━━━━━━━━━━━━━━━━━━\n"
        return msg


schedule_manager = ScheduleManager()
