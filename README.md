# Ekogram

**Ekogram** - это легкая библиотека для работы с Telegram Bot API версии 7.10. Она предоставляет простой и понятный интерфейс для отправки различных типов сообщений и обработки обновлений.

__Библиотека похожа на telebot, но она более простая и подходит для разработки достаточно сложных проектов__

## Установка
```bash
pip install ekogram
```

## Краткое использование:
```python
from ekogram import Bot, Markup
import time

#Пожалуйста, убедитесь, что вы заменили 'YOUR_TOKEN' на ваш токен бота Telegram
bot = Bot('YOUR_TOKEN')

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_message(message.chat.id, 'Привет, я бот на модуле Telegrin!')

@bot.meessage_handler(content_types=['text']
def text_handler(message):
    buttons = [{'text': 'Кнопка 1', 'callback_data': '1'}, {'text': 'Кнопка 2', 'callback_data': '2'}, {'text': 'Кнопка 3', 'callback_data': '3'}]
    reply_markup = Markup.create_inline_keyboard(buttons, row_width=2)
    p = bot.reply_message(message.chat.id, f"Выберите кнопку {message.from_user.first_name}:", reply_markup=reply_markup)
    bot.edit_message_text(p.chat.id, message_id=p.message_id, text="Окей, шучу")
    time.sleep(3)
    bot.edit_message_reply_markup(p.chat.id, message_id=p.message_id)

@bot.callback_query_handler(func=lambda call: True)
def handle_button_1(call):
    if call.data == '1':
        bot.answer_callback_query(call.id, text="Вы нажали кнопку 1!")
    elif call.data == '2':
        bot.answer_callback_query(call.id, text="Вы нажали кнопку 2!")
    elif call.data == '3':
        bot.answer_callback_query(call.id, text="Вы нажали кнопку 3!")

@bot.callback_query_handler(data="1")
def handle_button_1(call):
    bot.answer_callback_query(call.id, text="Вы нажали кнопку 1!")

bot.polling()
```

## Лицензия
Telegrin распространяется под лицензией MIT.

## Контакты
Если у вас есть вопросы или предложения, пожалуйста, напишите нам: siriteamrs@gmail.com

## Обратная связь
**Если у вас есть еще вопросы, пожалуйста, дайте мне знать!**
