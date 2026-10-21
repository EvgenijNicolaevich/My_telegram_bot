import telebot
from datetime import datetime

# ===== НАСТРОЙКИ БОТА=====

TOKEN = "TOKEN_BOT" # В ковычки запешите токен своего telegram бота (можно бесплатно получить на @BotFather)
OWNER_ID = 1234567890 # Замени на свой Telegram ID (можно узнать на @UserInfo)

bot = telebot.TeleBot(TOKEN)

waiting_for_message = set() # Храним информацию о пользователе


# ===== ПРИВЕТСТВИЕ БОТА =====

@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name or "Здравствуйте"

    text = (
        f"Здравствуйте, {name}!\n\n"
        "👔 Вы обратились к личному секретарю "
        "Евгения Николаевича.\n\n"
        "💬 Если вы хотите передать ему сообщение, "
        "напишите его следующим сообщением.\n\n"
        "📩 Я передам ваше сообщение Евгению Николаевичу.\n\n"
        "⚠️ Если вопрос срочный, свяжитесь с Евгением "
        "Николаевичем по телефону, если у вас есть его номер. "
        "Если номера у вас нет, пожалуйста, оставьте сообщение "
        "через бота.\n\n"
        "✍️ Напишите ваше сообщение:"
    )

    waiting_for_message.add(message.from_user.id)
    bot.send_message(message.chat.id, text)


# ===== ОТМЕНА ПЕРЕДАЧИ СООБЩЕНИЯ=====

@bot.message_handler(commands=['cancel'])
def cancel(message):
    waiting_for_message.discard(message.from_user.id) # Удаляем информацию о пользователе

    bot.send_message(
        message.chat.id,
        "Передача сообщения отменена. "
        "Если понадобится, обращайтесь!"
    )


# ===== ПОЛУЧЕНИЕ СООБЩЕНИЯ =====

@bot.message_handler(
    func=lambda message: message.from_user.id in waiting_for_message,
    content_types=['text']
)
def receive_message(message):
    user = message.from_user

    # Если впереди стоит "/" обрабатываем команды как обычные сообщения
    if message.text.startswith('/'):
        bot.send_message(
            message.chat.id,
            "Чтобы отменить отправку, напишите /cancel.\n"
            "Чтобы начать заново, напишите /start."
        )
        return

    
# ===== ОТПРАВКА СООБЩЕНИЯ БОТОМ =====
    
    name = user.first_name or "Не указано"
    surname = user.last_name or ""
    username = f"@{user.username}" if user.username else "нет"
    user_id = user.id
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    notification = (
        "📩 НОВОЕ СООБЩЕНИЕ ДЛЯ ЕВГЕНИЯ НИКОЛАЕВИЧА\n\n"
        f"👤 Отправитель: {name} {surname}\n"
        f"🔹 Username: {username}\n"
        f"🆔 Telegram ID: {user_id}\n"
        f"🕒 Время: {current_time}\n\n"
        "💬 Текст сообщения:\n"
        f"{message.text}"
    )

    try:
        # Отправляем сообщение владельцу
        bot.send_message(OWNER_ID, notification)

        # Подтверждаем отправителю
        bot.send_message(
            message.chat.id,
            "✅ Спасибо! Ваше сообщение принято.\n\n"
            "Я передам его Евгению Николаевичу.\n\n"
            "Если захотите передать ещё одно сообщение, "
            "напишите /start."
        )

        waiting_for_message.discard(user.id)

    except Exception as err:
        print("Ошибка отправки:", err)

        bot.send_message(
            message.chat.id,
            "⚠️ Не удалось передать сообщение. "
            "Пожалуйста, попробуйте позже."
        )


# ===== ЗАПУСК БОТА =====

if __name__ == '__main__': # Проверяем как запущен файл
    print("Секретарь Евгения Николаевича запущен!")
    bot.infinity_polling(skip_pending=True)
