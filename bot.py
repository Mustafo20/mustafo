from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройки
TOKEN = "8011265796:AAHSpiSkcdZyQ6afqrGK5GA6FKFEW5JtznE"
CHANNEL_USERNAME = "https://t.me/Isl_Cargo_Urok"  # Замените на юзернейм вашего канала
PDF_PATH = "C:/Users/Administrator/Desktop/Frame 171 (4).pdf"  # Укажите путь к вашему PDF

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Приветствие
    await update.message.reply_text("📄Маълумоти бештар дар бораи isl cargo:")

    # Отправка PDF
    try:
        with open(PDF_PATH, "rb") as pdf:
            await update.message.reply_document(document=pdf, filename="Маълумот.pdf")
    except FileNotFoundError:
        await update.message.reply_text("❌ Ошибка: PDF файл не найден.")

    # Кнопка "Дальше"
    keyboard = [[InlineKeyboardButton("➡️ Давом додан", callback_data="next_1")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Тугмаи 'Давом-ро' зер кунед:", reply_markup=reply_markup)

# Обработка кнопок
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    # Ответить на callback query сразу, чтобы избежать тайм-аута
    await query.answer()

    if query.data == "next_1":
        keyboard = [[InlineKeyboardButton("📦 Адресро равон кунед", callback_data="next_2")]]
        await query.edit_message_text(
            "Барои давом додан сараввал адреси моро дар программаи Pinduoduo ворид кунед.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "next_2":
        await query.edit_message_text(
            "📦 Адрес складов:\n\n"
            "收货人：Ном\n"
            "联系：13020143323\n"
            "浙江省金华市义乌市苏溪后山邬一区58栋1号仓库50\n"
            "(Dushanbe, номер, имя)"
        )

        keyboard = [[InlineKeyboardButton("✅Обуна шудам", callback_data="continue")]]
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"Хохиш мекунем дар Telegram-канали мо обуна шавед: {CHANNEL_USERNAME}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "continue":
        await query.edit_message_text("✅Рахмат барои обуна шудан!")

        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Агар намедонед чи тавр дар Pinduoduo адресро ворид кунед видеохоро тамошо кунед 👇"
        )

        keyboard = [
            [InlineKeyboardButton("Тарзи ворид кардани адресс", url="https://example.com/video1")],
            [InlineKeyboardButton("Скачать на Андроид", url="https://example.com/video2")]
        ]

        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите одно из видео ниже для продолжения:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# Запуск бота
def main():
    application = Application.builder().token(TOKEN).read_timeout(30).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_button))

    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()
