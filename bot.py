#!/usr/bin/env python3

import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
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
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n"
        f"Я WISEACRE — бот для студентов.\n"
        f"Чтобы посмотреть расписание, напиши:\n"
        f"/raspisanie или просто 'расписание 15.12.2025'"
    )


async def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "📘 Доступные команды:\n"
        "/start — запустить бота\n"
        "/help — список команд\n"
        "/raspisanie — показать пары на сегодня\n"
        "Или просто напиши: расписание или расписание 15.12.2025"
    )
    await update.message.reply_text(help_text)


async def schedule_command(update: Update, context: CallbackContext) -> None:
    user_input = context.args
    if not user_input:
        message = schedule_manager.get_today_schedule()
    else:
        date_str = user_input[0]
        message = schedule_manager.get_schedule_for_date(date_str)
    await update.message.reply_text(message)


async def schedule_text(update: Update, context: CallbackContext) -> None:
    """Реакция на сообщение, содержащее слово 'расписание'"""
    text = update.message.text.lower().strip()
    if text.startswith("расписание"):
        parts = text.split()
        if len(parts) == 2:
            message = schedule_manager.get_schedule_for_date(parts[1])
        else:
            message = schedule_manager.get_today_schedule()
        await update.message.reply_text(message)


def main():
    if not TOKEN:
        raise ValueError("❌ Токен не найден! Укажи BOT_TOKEN в .env")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("raspisanie", schedule_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, schedule_text))

    print("🤖 Бот WISEACRE запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
