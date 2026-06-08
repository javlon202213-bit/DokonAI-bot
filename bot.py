import os
import telebot
from openai import OpenAI

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

SYSTEM_PROMPT = """Siz DokonAI — o'zbek tilidagi online do'kon uchun AI yordamchisiz.
Do'kon haqida:
- Mahsulotlar: kiyim-kechak, elektronika, uy jihozlari
- Narxlar: 50,000 dan 5,000,000 so'mgacha
- Yetkazib berish: Toshkentda 1 kun, viloyatlarga 2-3 kun
- Bepul yetkazib berish: 500,000 so'mdan yuqori
- To'lov: Payme, Click, Uzcard, Humo, naqd
- Qaytarish: 14 kun ichida
- Ish vaqti: 09:00-21:00
Qisqa va do'stona javob bering. Faqat o'zbek tilida."""

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Assalomu alaykum! DokonAI xizmatiga xush kelibsiz! Savolingizni yozing.")

@bot.message_handler(func=lambda m: True)
def handle(message):
    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct:free",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message.text}
        ]
    )
    bot.reply_to(message, response.choices[0].message.content)

bot.polling()
