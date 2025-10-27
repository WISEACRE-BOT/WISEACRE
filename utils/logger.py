#!/usr/bin/env python3
# utils/logger.py

import os
import json
from datetime import datetime


class UserLogger:
    def __init__(self, logs_dir: str = "data/logs"):
        self.logs_dir = logs_dir
        self._ensure_logs_directory()
    
    def _ensure_logs_directory(self):
        """Создает папку для логов если ее нет"""
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
    
    def _get_user_log_file(self, student_id: str) -> str:
        """Возвращает путь к файлу лога пользователя"""
        return os.path.join(self.logs_dir, f"{student_id}.json")
    
    def log_message(self, student_id: str, message_type: str, content: str):
        """Логирует сообщение пользователя"""
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": message_type,  # "command", "message", "authentication"
            "content": content
        }
        
        log_file = self._get_user_log_file(student_id)
        
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    
    def log_authentication(self, student_id: str, success: bool):
        """Логирует попытку аутентификации"""
        status = "successful" if success else "failed"
        self.log_message(student_id, "authentication", f"Authentication {status}")


logger = UserLogger()
