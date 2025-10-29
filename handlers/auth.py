#!/usr/bin/env python3
# handlers/auth.py

from telegram import Update
from telegram.ext import ContextTypes
from database import db
from utils.logger import logger


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    
    logger.log_command(user, "start")
    
    welcome_text = """
🎓 *На связи Умник!*

🔐 *Для доступа к функциям необходимо пройти аутентификацию.*

Пожалуйста, введите ваш номер студенческого билета:
"""
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown')


async def handle_student_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ввода номера студбилета"""
    user = update.effective_user
    student_id = update.message.text
    
    logger.log_text_message(user, f"Введен студбилет: {student_id}")
    
    success, message = db.authenticate_student(student_id, user)
    
    logger.log_authentication(user, student_id, success, message)
    
    if success:
        context.user_data['student_id'] = student_id
        context.user_data['authenticated'] = True
        
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
