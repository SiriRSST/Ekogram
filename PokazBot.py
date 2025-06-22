from ekogram import Bot, Markup, FreeGpt, FreeImg
import random, os

# Инициализация бота с токеном
bot = Bot("Bot-Token")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    user = message.from_user.first_name
    welcome_text = f"Привет, {user}!\nЯ бот-пример на ekogram.\nИспользуй /help для списка команд."
    bot.reply_message(message.chat.id, welcome_text)

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help_handler(message):
    commands = [
        "/start - Начать работу",
        "/help - Помощь и команды",
        "/art - Случайная картинка",
        "/btn - Тест кнопок"]
    bot.reply_message(message.chat.id, f"Доступные команды: \n{'\n'.join(commands)}")

# Обработчик для отправки картинок
@bot.message_handler(commands=['art'])
def pic_handler(message):
    image_url = FreeImg().art("random anime")
    if image_url:
        bot.reply_photo(message.chat.id, open("image.png", 'rb'), caption="Случайная картинка")
        os.remove("image.png")
    else:
        bot.reply_message(message.chat.id, "Не удалось загрузить картинку.")

# Обработчик для демонстрации кнопок
@bot.message_handler(commands=['btn'])
def button_handler(message):
    # Создаем inline-клавиатуру
    buttons = [{"text": "GitHub", "url": "https://github.com"}, {"text": "Telegram", "url": "tg://resolve?domain=telegram"}, {"text": "Показать ID", "callback_data": "show_id"}]
    markup = Markup.create_inline_keyboard(buttons)
    bot.reply_message(message.chat.id, "Выберите действие:", reply_markup=markup)

# Обработчик callback-запросов
@bot.callback_query_handler(data="show_id")
def callback_handler(callback_query):
    user_id = callback_query.from_user.id
    bot.answer_callback_query(callback_query.id, f"Ваш ID: {user_id}")

# Обработчик текстовых сообщений
@bot.message_handler()
def text_handler(message):
    zapros = FreeGpt().toolchat(prompt=message.text, model_index=random.randint(0, 20))
    bot.reply_message(message.chat.id, zapros, reply_to_message_id=message.message_id)

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.always_polling()