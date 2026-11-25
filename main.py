import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8080))
RAILWAY_STATIC_URL = os.environ.get("RAILWAY_PUBLIC_DOMAIN") or os.environ.get("RAILWAY_STATIC_URL", "")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🔍 Check SB Pay Status", callback_data='check_status')],
        [InlineKeyboardButton("📖 User Guide", callback_data='help')],
        [InlineKeyboardButton("ℹ️ About This Bot", callback_data='about')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = (
        f"Hello {user.first_name}!\n\n"
        "I am your SB Pay Reminder Assistant.\n"
        "I can help you quickly check SB Pay service status and provide basic usage guidance.\n\n"
        "Please select an option below:"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'check_status':
        await query.edit_message_text(
            text="✅ SB Pay Service Status: **Normal**\n\n"
                 "Current time: Available\n"
                 "System maintenance: No scheduled maintenance\n\n"
                 "If you encounter issues, please visit the official channel for updates.",
            parse_mode='Markdown'
        )
    elif query.data == 'help':
        await query.edit_message_text(
            text="📖 **User Guide**\n\n"
                 "1. Click 'Check SB Pay Status' to get real-time service availability.\n"
                 "2. This bot does not collect personal information.\n"
                 "3. For specific financial operations, please use the official SB Pay app.",
            parse_mode='Markdown'
        )
    elif query.data == 'about':
        await query.edit_message_text(
            text="ℹ️ **About**\n\n"
                 "This is a lightweight assistant bot designed to provide SB Pay-related service status information.\n"
                 "It does not represent any official institution.\n\n"
                 "Version: 1.0.0",
            parse_mode='Markdown'
        )

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    if RAILWAY_STATIC_URL:
        webhook_url = f"https://{RAILWAY_STATIC_URL}/{TOKEN}"
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN,
            webhook_url=webhook_url
        )
    else:
        application.run_polling()

if __name__ == '__main__':
    main()
