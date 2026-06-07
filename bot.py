import os
import telebot
import anthropic

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

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
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": message.text}]
    )
    bot.reply_to(message, response.content[0].text)

bot.polling()
