import os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

bot = telebot.TeleBot(TOKEN)

services = {
    "vip": ("VIP-чаты", 1500),
    "private": ("Приватные чаты", 2999),
    "mp": ("Анкеты с МП", 2500),
    "nomp": ("Анкеты без МП", 6000),
    "ads": ("Реклама", None)
}

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛍 Каталог услуг", "📦 Мои заказы")
    markup.add("💬 Поддержка")
    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Выберите раздел:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "🛍 Каталог услуг")
def catalog(message):
    markup = types.InlineKeyboardMarkup()
    for key, (name, price) in services.items():
        label = f"{name} — {price} ₽" if price else f"{name} — по договорённости"
        markup.add(types.InlineKeyboardButton(label, callback_data=key))
    bot.send_message(message.chat.id, "Выберите услугу:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in services)
def order(call):
    name, price = services[call.data]
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        f"Вы выбрали: {name}\nСтоимость: {price or 'по договорённости'}"
    )
    if ADMIN_ID:
        bot.send_message(
            int(ADMIN_ID),
            f"Новый запрос от @{call.from_user.username or 'без username'}: {name}"
        )

@bot.message_handler(func=lambda m: m.text == "📦 Мои заказы")
def orders(message):
    bot.send_message(message.chat.id, "История заказов пока пуста.")

@bot.message_handler(func=lambda m: m.text == "💬 Поддержка")
def support(message):
    bot.send_message(message.chat.id, "Напишите администратору: @ZnMoscowShopBot")

bot.infinity_polling()
