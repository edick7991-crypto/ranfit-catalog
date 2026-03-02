from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8634832877:AAHGNPabpx9wkoinobilY5mmnF1U_m12yD0"
MANAGER_ID = 123456789  # вставь сюда Telegram ID менеджера

WEBAPP_URL = "http://127.0.0.1:8000/index.html"  # пока локально

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Каталог 👟", web_app=WebAppInfo(WEBAPP_URL))]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Вітаємо! Оберіть:", reply_markup=markup)

# Получаем событие заказа из Web App
async def webapp_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.web_app_data:
        order_name = update.message.web_app_data.data
        await context.bot.send_message(
            chat_id=MANAGER_ID,
            text=f"Нове замовлення: {order_name} від {update.message.from_user.full_name}"
        )
        await update.message.reply_text(f"Ваше замовлення на '{order_name}' відправлено менеджеру ✅")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("webapp_data", webapp_handler))  # для получения данных
    print("Бот запущен! Напишите /start в Telegram.")
    app.run_polling()