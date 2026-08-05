from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import json
import os

users = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users[update.effective_user.id] = {"step": "name"}

    await update.message.reply_text(
        "سلام! به ربات کاریابی خوش اومدی.\n\nلطفاً نام و نام خانوادگی خود را وارد کنید."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in users:
        await update.message.reply_text("ابتدا /start را بزنید.")
        return

    if users[user_id]["step"] == "name":
        users[user_id]["name"] = text
        users[user_id]["step"] = "job"

        await update.message.reply_text(
            "شغل یا تخصص خود را وارد کنید."
        )

    elif users[user_id]["step"] == "job":
        users[user_id]["job"] = text
        users[user_id]["step"] = "description"

        await update.message.reply_text(
            "لطفاً چند خط درباره مهارت‌ها و سوابق خود بنویسید."
        )

    elif users[user_id]["step"] == "description":
        users[user_id]["description"] = text

        new_user = {
            "name": users[user_id]["name"],
            "job": users[user_id]["job"],
            "description": users[user_id]["description"]
        }

        data = []

        if os.path.exists("users.json"):
            with open("users.json", "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except:
                    data = []

        data.append(new_user)

        with open("users.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        await update.message.reply_text(
            "اطلاعات شما با موفقیت ثبت شد ✅\n\n"
            "برای مشاهده فرصت‌های شغلی بیشتر به کانال ما مراجعه کنید:\n"
            "@test"
        )


app = Application.builder().token("8958860652:AAHAaWtbsnTIx_nmT6asLH5Eordz2lJ1Cyw").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

import asyncio

async def main():
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

asyncio.run(main())
