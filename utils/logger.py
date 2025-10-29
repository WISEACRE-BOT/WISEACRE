#!/usr/bin/env python3
# utils/logger.py

import os
import json
from datetime import datetime
from telegram import User


class UserLogger:
    def __init__(self, logs_dir: str = "data/logs"):
        self.logs_dir = logs_dir
        self._ensure_logs_directory()
    
    def _ensure_logs_directory(self):
        """Создает папку для логов если ее нет"""
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
    
    def _get_user_log_file(self, user: User) -> str:
        """Возвращает путь к файлу лога пользователя"""
        username = user.username or f"user_{user.id}"
        return os.path.join(self.logs_dir, f"{username}.txt")
    
    def log_message(self, user: User, message_type: str, content: str):
        """Логирует сообщение пользователя в текстовый файл"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message_type.upper()}: {content}\n"
        
        log_file = self._get_user_log_file(user)
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")  
    
    def log_authentication(self, user: User, student_id: str, success: bool, message: str):
        """Логирует попытку аутентификации"""
        status = "SUCCESS" if success else "FAILED"
        self.log_message(user, "AUTH", f"{status} - Студбилет: {student_id} - {message}")
    
    def log_command(self, user: User, command: str):
        """Логирует команду пользователя"""
        self.log_message(user, "COMMAND", f"/{command}")
    
    def log_text_message(self, user: User, message: str):
        """Логирует текстовое сообщение пользователя"""
        self.log_message(user, "MESSAGE", message)


logger = UserLogger()
