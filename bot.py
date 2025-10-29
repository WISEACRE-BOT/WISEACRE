#!/usr/bin/env python3

import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackContext,
)
from utils.schedule_manager import schedule_manager
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")  

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start_command(update: Update, context: CallbackContext) -> None:
    """Приветствие при старте"""
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n"
        f"Я WISEACRE — бот для студентов.\n"
        f"Чтобы посмотреть расписание, напиши:\n"
        f"/расписание или /расписание 15.12.2025"
    )


async def help_command(update: Update, context: CallbackContext) -> None:
    """Помощь по командам"""
    help_text = (
        "📘 Доступные команды:\n"
        "/start — запустить бота\n"
        "/help — список команд\n"
        "/расписание — показать пары на сегодня\n"
        "/расписание <дата> — пары на выбранную дату (в формате ДД.ММ.ГГГГ)\n"
    )
    await update.message.reply_text(help_text)


async def schedule_command(update: Update, context: CallbackContext) -> None:
    """Команда /расписание [дата] — показывает пары на указанную дату или сегодня"""
    user_input = context.args
    if not user_input:
        message = schedule_manager.get_today_schedule()
    else:
        date_str = user_input[0]
        message = schedule_manager.get_schedule_for_date(date_str)

    await update.message.reply_text(message)


def main():
    """Точка входа"""
    if not TOKEN:
        raise ValueError("❌ Токен не найден! Укажи BOT_TOKEN в .env")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("расписание", schedule_command))

    print("🤖 Бот WISEACRE запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
