import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


TOKEN = "..."
WEB_APP_URL = "..."


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)



# /set 
async def set_banana(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 3:
            await update.message.reply_text("❌ Формат: /set ДАТА @ник КОЛИЧЕСТВО")
            return

        date, nick, amount = context.args[0], context.args[1], context.args[2]
        params = {"action": "add", "date": date, "nick": nick, "amount": amount}
        r = requests.post(WEB_APP_URL, json=params, timeout=10)

        if "Added" in r.text:
            await update.message.reply_text(f"✅ Добавлено: {date} {nick} +{amount}")
        else:
            await update.message.reply_text("⚠️ Ошибка при добавлении данных.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")

# /balance 
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 1:
            await update.message.reply_text("❌ Формат: /balance @ник")
            return

        nick = context.args[0]
        params = {"action": "balance", "nick": nick}
        r = requests.post(WEB_APP_URL, json=params, timeout=10)
        text = r.text

        if text.startswith("BALANCE:"):
            total = text.split(":")[1]
            await update.message.reply_text(f"🍌 Баланс {nick}: {total}")
        else:
            await update.message.reply_text("⚠️ Не удалось получить баланс.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")

# /remove 
async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 2:
            await update.message.reply_text("❌ Формат: /remove ДАТА @ник")
            return

        date, nick = context.args[0], context.args[1]
        params = {"action": "remove", "date": date, "nick": nick}
        r = requests.post(WEB_APP_URL, json=params, timeout=10)
        text = r.text.strip()

        if text == "SUCCESS":
            await update.message.reply_text(f"🗑 Удалено: {date} {nick}")
        elif text == "NOT_FOUND":
            await update.message.reply_text(f"⚠️ Запись {date} {nick} не найдена.")
        else:
            await update.message.reply_text("⚠️ Ошибка при удалении.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")

# /removeall 
async def remove_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 1:
            await update.message.reply_text("❌ Формат: /removeall @ник")
            return

        nick = context.args[0]
        params = {"action": "removeall", "nick": nick}
        r = requests.post(WEB_APP_URL, json=params, timeout=10)
        text = r.text.strip()

        if text.startswith("SUCCESS:"):
            count = text.split(":")[1]
            await update.message.reply_text(f"🗑 Удалено всех записей для {nick}: {count}")
        elif text == "NOT_FOUND":
            await update.message.reply_text(f"⚠️ Для {nick} записей не найдено.")
        else:
            await update.message.reply_text("⚠️ Ошибка при удалении.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")

# /history 
async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 1:
            await update.message.reply_text("❌ Формат: /history @ник")
            return

        nick = context.args[0]
        params = {"action": "history", "nick": nick}
        r = requests.post(WEB_APP_URL, json=params, timeout=10)
        text = r.text.strip()

        if text.lower().startswith("not_found"):
            await update.message.reply_text(f"⚠️ Для {nick} записей не найдено.")
        elif text.lower().startswith("error"):
            await update.message.reply_text("⚠️ Ошибка при получении истории.")
        else:
            await update.message.reply_text(f"📜 История {nick}:\n\n{text}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")

# start
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("set", set_banana))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("remove", remove))
    app.add_handler(CommandHandler("removeall", remove_all))
    app.add_handler(CommandHandler("history", history))

    print("✅ Бот запущен и готов к работе!")
    app.run_polling()

if __name__ == "__main__":
    main()
