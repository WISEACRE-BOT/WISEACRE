#!/usr/bin/env python3

import hashlib
import os
from typing import Tuple


class StudentDatabase:
    def __init__(self, data_file: str = "data/allowed_students.txt"):
        self.data_file = data_file
        self.data_dir = "data"
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Создает папку data если ее нет"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _hash_student_id(self, student_id: str) -> str:
        """Хеширует номер студбилета для безопасности"""
        return hashlib.sha256(student_id.strip().encode()).hexdigest()
    
    def add_student(self, student_id: str) -> bool:
        """Добавляет номер студбилета в базу (еще не занят)"""
        student_hash = self._hash_student_id(student_id)
        
        if self.is_student_exists(student_id):
            return False
        
        with open(self.data_file, "a", encoding="utf-8") as f:
            f.write(f"{student_hash}:свободен\n")
        
        return True
    
    def is_student_exists(self, student_id: str) -> bool:
        """Проверяет существует ли номер студбилета в базе"""
        student_hash = self._hash_student_id(student_id)
        
        if not os.path.exists(self.data_file):
            return False
        
        with open(self.data_file, "r", encoding="utf-8") as f:
            for line in f:
                stored_hash, status = line.strip().split(":")
                if stored_hash == student_hash:
                    return True
        return False
    
    def authenticate_student(self, student_id: str) -> Tuple[bool, str]:
        """Аутентифицирует студента и помечает номер как занятый"""
        student_hash = self._hash_student_id(student_id)
        
        if not os.path.exists(self.data_file):
            return False, "База данных не найдена"
        
        lines = []
        found = False
        result_message = ""
        
        with open(self.data_file, "r", encoding="utf-8") as f:
            for line in f:
                stored_hash, status = line.strip().split(":")
                if stored_hash == student_hash:
                    found = True
                    if status == "свободен":
                        lines.append(f"{stored_hash}:занят\n")
                        result_message = "Успешная аутентификация!"
                    else:
                        result_message = "Этот номер уже используется"
                        lines.append(line)
                else:
                    lines.append(line)
        
        if found:
            with open(self.data_file, "w", encoding="utf-8") as f:
                f.writelines(lines)
            return (result_message == "Успешная аутентификация!"), result_message
        else:
            return False, "Номер студбилета не найден"
    
    def get_student_count(self) -> Tuple[int, int]:
        """Возвращает общее количество номеров и количество свободных"""
        if not os.path.exists(self.data_file):
            return 0, 0
        
        total = 0
        free = 0
        
        with open(self.data_file, "r", encoding="utf-8") as f:
            for line in f:
                total += 1
                _, status = line.strip().split(":")
                if status == "свободен":
                    free += 1
        
        return total, free
    
db = StudentDatabase()
