# Ekogram

**Ekogram** - это легкая библиотека для работы с Telegram Bot API версии 7.10. Она предоставляет простой и понятный интерфейс для отправки различных типов сообщений и обработки обновлений.

__Библиотека похожа на telebot, но она более простая и подходит для разработки достаточно сложных проектов__

## Установка
```bash
pip install ekogram
```

## Общий пример использования:
```python
from ekogram import Bot, Markup
import time

bot = Bot('You_Bot_Token')

@bot.message_handler(content_types=['new_chat_member'])
def hello_mention(message):
    new_member = message.new_chat_member.first_name
    new_id = message.new_chat_member.id
    chat_id = message.chat.id
    print(new_member)
    if new_id == bot.get_me().id:
        bot.reply_message(text=f"Привет, меня зовут бот", mode="Markdown")
    else:
        bot.reply_message(chat_id, text=f"Привет [{str(new_member).replace('[', '').replace(']', '')}](tg://user?id={new_id})!", mode="Markdown")


@bot.message_handler(content_types=['left_chat_member'])
def godbye_mention(message):
    tot_name = message.left_chat_member.first_name
    tot_id = message.left_chat_member.id
    chat_id = message.chat.id
    bot.reply_message(chat_id, f"[{str(tot_name).replace('[', '').replace(']', '')}](tg://user?id={tot_id}) покинул(а) беседу", mode="Markdown")


@bot.message_handler(commands=['start'])
def start(message):
    buttons = [{'text': 'Кнопка 1', 'callback_data': '1'}, {'text': 'Кнопка 2', 'callback_data': '2'}, {'text': 'Кнопка 3', 'callback_data': '3'}]
    reply_markup = Markup.create_inline_keyboard(buttons, row_width=2)
    p = bot.reply_message(message.chat.id, f"Выберите кнопку {message.from_user.first_name}:", reply_markup=reply_markup)
    bot.edit_message_text(p.chat.id, message_id=p.message_id, text="Окей, шучу")
    bot.edit_message_reply_markup(p.chat.id, message_id=p.message_id, reply_markup=reply_markup)


@bot.message_handler(commands=['help'])
def help(message):
    buttonss = [{'text': 'Кнопка 1'}, {'text': 'Кнопка 2'}, {'text': 'Кнопка 3'}]
    reply_markup = Markup.create_reply_keyboard(buttonss, row_width=1)
    bot.reply_message(message.chat.id, "Кнопки:", reply_markup=reply_markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_button_1(call):
    if call.data == '1':
        bot.answer_callback_query(call.id, text="Вы нажали кнопку 1!")
    elif call.data == '2':
        bot.answer_callback_query(call.id, text="Вы нажали кнопку 2!")
    elif call.data == '3':
        bot.answer_callback_query(call.id, text="Вы нажали кнопку 3!")

@bot.message_handler(content_types=['text'])
def ms_obrabotka(ms):
    chat_id = ms.chat.id
    message_id = ms.message_id
    if ms.text == 'Кнопка 1':
        bot.reply_message(chat_id, 'Вы нажали кнопку 1!', reply_to_message_id=message_id)
    if ms.text == 'Кнопка 2':
        bot.reply_message(chat_id, 'Вы нажали кнопку 2!', reply_to_message_id=message_id)
    if ms.text == 'Кнопка 3':
        bot.reply_message(chat_id, 'Вы нажали кнопку 3!', reply_to_message_id=message_id)
    if ms.text == 'Привет':
        bot.reply_message(chat_id, 'Привет, я бот!', reply_to_message_id=message_id)


@bot.message_handler(content_types=['photo'])
def handle_photo_message(message):
    chat_id = message.chat.id
    photo_id = message.photo[-1].file_id
    p = bot.get_file(photo_id)
    bot.download_file(p, p.file_path)
    bot.reply_photo(chat_id, photo=photo_id, reply_to_message_id=message.message_id, caption=f"`{photo_id}`", mode="Markdown")
    bot.delete_chat_photo(chat_id)


@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    chat_id = message.chat.id
    voice = message.voice.file_id
    bot.reply_voice(chat_id, voice=voice, reply_to_message_id=message.message_id, caption=f"`{voice}`", mode="Markdown")


@bot.message_handler(content_types=['document'])
def handle_document_message(message):
    chat_id = message.chat.id
    document = message.document.file_id
    p = bot.get_file(document)
    bot.download_file(p, './document.txt')
    bot.reply_document(chat_id, document=open('./document.txt', 'rb'), reply_to_message_id=message.message_id, caption=f"`{document}`", mode="Markdown")

@bot.message_handler(content_types=['video'])
def handle_video_message(message):
    chat_id = message.chat.id
    video = message.video.file_id
    p = bot.get_file(video)
    bot.download_file(p, './video.mp4')
    bot.reply_video(chat_id, video=open('./video.mp4', 'rb'), reply_to_message_id=message.message_id, caption=f"`{video}`", mode="Markdown")


@bot.message_handler(content_types=['audio'])
def handle_audio_message(message):
    chat_id = message.chat.id
    audio = message.audio.file_id
    p = bot.get_file(audio)
    bot.download_file(p, './audio.mp3')
    bot.reply_audio(chat_id, audio=open('./audio.mp3', 'rb'), reply_to_message_id=message.message_id, caption=f"`{audio}`", mode="Markdown")


@bot.message_handler(content_types=['video_note'])
def handle_video_note_message(message):
    chat_id = message.chat.id
    video_note = message.video_note.file_id
    p = bot.get_file(video_note)
    bot.download_file(p, './video_note.mp4')
    bot.reply_video_note(chat_id, video_note=open('./video_note.mp4', 'rb'), reply_to_message_id=message.message_id, caption=f"`{video_note}`", mode="Markdown")


@bot.message_handler(content_types=['sticker'])
def handle_sticker_message(message):
    chat_id = message.chat.id
    sticker = message.sticker.file_id
    p = bot.get_file(sticker)
    bot.download_file(p, './sticker.webp')
    bot.reply_sticker(chat_id, sticker=open('./sticker.webp', 'rb'), reply_to_message_id=message.message_id)


@bot.message_handler(content_types=['animation'])
def handle_animation_message(message):
    chat_id = message.chat.id
    animation = message.animation.file_id
    p = bot.get_file(animation)
    bot.download_file(p, './animation.mp4')
    bot.reply_animation(chat_id, animation=open('./animation.mp4', 'rb'), reply_to_message_id=message.message_id)    


bot.polling()
```

## Лицензия
Ekogram распространяется под лицензией MIT.

## Контакты
Если у вас есть вопросы или предложения, пожалуйста, напишите нам: siriteamrs@gmail.com

## Обратная связь
**Если у вас есть еще вопросы, пожалуйста, дайте мне знать!**
