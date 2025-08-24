import telebot

# Bu yerga o'z tokeningizni yozing
TOKEN = "8306982400:AAHS-OeM0Q0WCynBlLqLWdzOMGuQ-e_JiBw"
bot = telebot.TeleBot(TOKEN)

# Test savollari bazasi (hozircha bitta misol, keyin o'zingiz ko'paytirib borasiz)
questions = [
    {
        "question": "1-savol: Amir Temur qachon tug‘ilgan?",
        "options": ["A) 1336-yil", "B) 1350-yil", "C) 1405-yil", "D) 1380-yil"],
        "answer": "A"
    },
    {
        "question": "2-savol: Jadidchilik harakati qaysi asrda paydo bo‘lgan?",
        "options": ["A) XIX asr oxiri", "B) XVIII asr", "C) XX asr o‘rtalari", "D) XVII asr"],
        "answer": "A"
    }
]

# Foydalanuvchi qaysi savolni yechayotganini saqlash uchun
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "Assalom aleykum. Rahimova Gavharning Tarix fani test bazalar botiga xush kelibsiz!\n\n"
        "Testni boshlash uchun /test buyrug'ini bosing."
    )

@bot.message_handler(commands=['test'])
def start_test(message):
    user_data[message.chat.id] = 0  # 0-indeksdan boshlanadi
    send_question(message.chat.id)

def send_question(chat_id):
    index = user_data[chat_id]
    if index < len(questions):
        q = questions[index]
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for option in q["options"]:
            markup.add(option)
        bot.send_message(chat_id, q["question"], reply_markup=markup)
    else:
        bot.send_message(chat_id, "Test tugadi! 🎉")
        user_data.pop(chat_id)

@bot.message_handler(func=lambda message: True)
def check_answer(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        return

    index = user_data[chat_id]
    q = questions[index]
    user_answer = message.text[0].upper()  # A, B, C, D ni oladi

    if user_answer == q["answer"]:
        bot.send_message(chat_id, "✅ To‘g‘ri!")
    else:
        bot.send_message(chat_id, f"❌ Noto‘g‘ri! To‘g‘ri javob: {q['answer']}")

    user_data[chat_id] += 1
    send_question(chat_id)

# Botni doimiy ishlatish uchun
bot.polling()
