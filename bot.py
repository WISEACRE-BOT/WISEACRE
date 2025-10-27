#!/usr/bin/env python3

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN
from handlers.auth import start_command, handle_student_id


async def handle_other_messages(update: Update, context):
    """Обработчик других сообщений (после аутентификации)"""
    await update.message.reply_text("Обрабатываю ваше сообщение...")


def main():
    """Основная функция запуска бота"""
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_student_id))
    application.add_handler(MessageHandler(filters.TEXT, handle_other_messages))
    
    print("🤖 Бот WISEACRE запущен...")
    application.run_polling()


if __name__ == "__main__":
    main()
