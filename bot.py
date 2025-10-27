#!/usr/bin/env python3

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN


async def start_command(update: Update, context):
    """Обработчик команды /start - приветственное сообщение"""
    
    welcome_text = """
🎓 *На связи Умник!*

Этот бот создан специально для студентов вашего университета, чтобы облегчить повседневную академическую жизнь.



🔐 *Для доступа к функциям необходимо пройти аутентификацию.*

Пожалуйста, введите ваш номер студенческого билета:
"""
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown')


async def handle_message(update: Update, context):
    """Обработчик обычных сообщений"""
    await update.message.reply_text("Пока что я понимаю только команду /start ")


def main():
    """Основная функция запуска бота"""
    
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    print("🤖 Бот WISEACRE запущен...")
    application.run_polling()


if __name__ == "__main__":
    main()
