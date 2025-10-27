#!/usr/bin/env python3
# handlers/auth.py

from telegram import Update
from telegram.ext import ContextTypes
from database import db
from utils.logger import logger


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    
    welcome_text = """
🎓 *На связи Умник!*

Этот бот создан специально для студентов вашего университета, чтобы облегчить повседневную академическую жизнь.

🔐 *Для доступа к функциям необходимо пройти аутентификацию.*

Пожалуйста, введите ваш номер студенческого билета:
"""
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown')


async def handle_student_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ввода номера студбилета"""
    student_id = update.message.text
    
    # Логируем ввод номера
    logger.log_message(student_id, "message", f"Введен номер: {student_id}")
    
    success, message = db.authenticate_student(student_id)
    
    # Логируем результат аутентификации
    logger.log_authentication(student_id, success)
    
    if success:
        # Сохраняем student_id в контексте для будущих логов
        context.user_data['student_id'] = student_id
        
        welcome_text = """
✅ *Аутентификация успешна!*

Теперь вам доступны все функции бота!
"""
    else:
        welcome_text = f"""
❌ *Ошибка аутентификации*

{message}
"""
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown')
