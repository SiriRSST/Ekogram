import requests, json, os, time, re


class User:
    def __init__(self, user_id, is_bot=False, first_name=None, last_name=None, username=None, 
                 language_code=None, is_premium=None, added_to_attachment_menu=None, can_join_groups=None, 
                 can_read_all_group_messages=None, supports_inline_queries=None, can_connect_to_business=None, 
                 has_main_web_app=None):
        self.id = user_id
        self.is_bot = is_bot
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.language_code = language_code
        self.is_premium = is_premium
        self.added_to_attachment_menu = added_to_attachment_menu
        self.can_join_groups = can_join_groups
        self.can_read_all_group_messages = can_read_all_group_messages
        self.supports_inline_queries = supports_inline_queries
        self.can_connect_to_business = can_connect_to_business
        self.has_main_web_app = has_main_web_app

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data['id'],
            is_bot=data.get('is_bot', False),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            username=data.get('username'),
            language_code=data.get('language_code'),
            is_premium=data.get('is_premium'),
            added_to_attachment_menu=data.get('added_to_attachment_menu'),
            can_join_groups=data.get('can_join_groups'),
            can_read_all_group_messages=data.get('can_read_all_group_messages'),
            supports_inline_queries=data.get('supports_inline_queries'),
            can_connect_to_business=data.get('can_connect_to_business'),
            has_main_web_app=data.get('has_main_web_app')
        )

    def __repr__(self):
        return (f"User(id={self.id}, is_bot={self.is_bot}, first_name={self.first_name}, "
                f"last_name={self.last_name}, username={self.username}, language_code={self.language_code}, "
                f"is_premium={self.is_premium}, added_to_attachment_menu={self.added_to_attachment_menu}, "
                f"can_join_groups={self.can_join_groups}, can_read_all_group_messages={self.can_read_all_group_messages}, "
                f"supports_inline_queries={self.supports_inline_queries}, can_connect_to_business={self.can_connect_to_business}, "
                f"has_main_web_app={self.has_main_web_app})")


class Chat:
    def __init__(self, chat_id, chat_type, title=None, username=None, first_name=None, last_name=None, is_forum=None):
        self.id = chat_id
        self.type = chat_type
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.is_forum = is_forum

    @classmethod
    def from_dict(cls, data):
        return cls(
            chat_id=data['id'],
            chat_type=data['type'],
            title=data.get('title'),
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            is_forum=data.get('is_forum')
        )

    def __repr__(self):
        return (f"Chat(id={self.id}, type={self.type}, title={self.title}, username={self.username}, "
                f"first_name={self.first_name}, last_name={self.last_name}, is_forum={self.is_forum})")


class PhotoSize:
    def __init__(self, file_id, file_unique_id, width, height, file_size=None):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.file_size = file_size

    @classmethod
    def from_dict(cls, data):
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            width=data['width'],
            height=data['height'],
            file_size=data.get('file_size')
        )

    def __repr__(self):
        return (f"PhotoSize(file_id={self.file_id}, file_unique_id={self.file_unique_id}, "
                f"width={self.width}, height={self.height}, file_size={self.file_size})")


class Photo:
    def __init__(self, file_id, file_unique_id, width, height):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height

    @classmethod
    def from_dict(cls, data):
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            width=data['width'],
            height=data['height']
        )


class Audio:
    def __init__(self, file_id, file_unique_id, duration, performer=None, title=None, thumbnail=None):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.duration = duration
        self.performer = performer
        self.title = title
        self.thumbnail = PhotoSize.from_dict(thumbnail) if thumbnail else None

    @classmethod
    def from_dict(cls, data):
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            duration=data['duration'],
            performer=data.get('performer'),
            title=data.get('title'),
            thumbnail=data.get('thumbnail')
        )


class Voice:
    def __init__(self, file_id, file_unique_id, duration, mime_type=None, file_size=None, thumbnail=None):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.duration = duration
        self.mime_type = mime_type
        self.file_size = file_size
        self.thumbnail = PhotoSize.from_dict(thumbnail) if thumbnail else None

    @classmethod
    def from_dict(cls, data):
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            duration=data['duration'],
            mime_type=data.get('mime_type'),
            file_size=data.get('file_size'),
            thumbnail=data.get('thumbnail')
        )


class Video:
    def __init__(self, file_id, file_unique_id, duration, width, height, thumbnail=None):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.duration = duration
        self.width = width
        self.height = height
        self.thumbnail = PhotoSize.from_dict(thumbnail) if thumbnail else None

    @classmethod
    def from_dict(cls, data):
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            duration=data['duration'],
            width=data['width'],
            height=data['height'],
            thumbnail=data.get('thumbnail')
        )
    

class VideoNote:
    def __init__(self, file_id, file_unique_id, duration, length, thumbnail=None, file_size=None):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.duration = duration
        self.length = length
        self.thumbnail = PhotoSize.from_dict(thumbnail) if thumbnail else None
        self.file_size = file_size

    @classmethod
    def from_dict(cls, data):
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            duration=data['duration'],
            length=data['length'],
            thumbnail=data.get('thumbnail'),
            file_size=data.get('file_size')
        )

    def __repr__(self):
        return (f"VideoNote(file_id={self.file_id}, file_unique_id={self.file_unique_id}, "
                f"duration={self.duration}, length={self.length}, thumbnail={self.thumbnail}, "
                f"file_size={self.file_size})")


class Animation:
    def __init__(self, file_id, file_unique_id, width, height, duration, thumbnail=None, file_name=None, mime_type=None, file_size=None):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.duration = duration
        self.thumbnail = PhotoSize.from_dict(thumbnail) if thumbnail else None
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size

    @classmethod
    def from_dict(cls, data):
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            width=data['width'],
            height=data['height'],
            duration=data['duration'],
            thumbnail=data.get('thumbnail'),
            file_name=data.get('file_name'),
            mime_type=data.get('mime_type'),
            file_size=data.get('file_size')
        )


class Dice:
    def __init__(self, emoji, value):
        self.emoji = emoji
        self.value = value

    @classmethod
    def from_dict(cls, data):
        return cls(
            emoji=data['emoji'],
            value=data['value']
        )


class Sticker:
    def __init__(self, file_id, file_unique_id, width, height, is_animated, is_video, thumbnail=None):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.is_animated = is_animated
        self.is_video = is_video
        self.thumbnail = PhotoSize.from_dict(thumbnail) if thumbnail else None

    @classmethod
    def from_dict(cls, data):
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            width=data['width'],
            height=data['height'],
            is_animated=data.get('is_animated', False),
            is_video=data.get('is_video', False),
            thumbnail=data.get('thumbnail')
        )


class Document:
    def __init__(self, file_id, file_unique_id, file_name=None, mime_type=None, file_size=None, thumbnail=None):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
        self.thumbnail = PhotoSize.from_dict(thumbnail) if thumbnail else None

    @classmethod
    def from_dict(cls, data):
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            file_name=data.get('file_name'),
            mime_type=data.get('mime_type'),
            file_size=data.get('file_size'),
            thumbnail=data.get('thumbnail')
        )

    def __repr__(self):
        return (f"Document(file_id={self.file_id}, file_unique_id={self.file_unique_id}, "
                f"file_name={self.file_name}, mime_type={self.mime_type}, "
                f"file_size={self.file_size}, thumb={self.thumb}, thumbnail={self.thumbnail})")
    

class File:
    def __init__(self, file_id, file_unique_id, file_size, file_path=None):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_size = file_size
        self.file_path = file_path

    @classmethod
    def from_dict(cls, data):
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            file_size=data['file_size'],
            file_path=data.get('file_path')
        )


class WebhookInfo:
    def __init__(self, url=None, has_custom_certificate=None, pending_update_count=None,
                 last_error_date=None, last_error_message=None, max_connections=None,
                 allowed_updates=None):
        self.url = url
        self.has_custom_certificate = has_custom_certificate
        self.pending_update_count = pending_update_count
        self.last_error_date = last_error_date
        self.last_error_message = last_error_message
        self.max_connections = max_connections
        self.allowed_updates = allowed_updates

    @classmethod
    def from_dict(cls, data):
        return cls(
            url=data.get('url'),
            has_custom_certificate=data.get('has_custom_certificate'),
            pending_update_count=data.get('pending_update_count'),
            last_error_date=data.get('last_error_date'),
            last_error_message=data.get('last_error_message'),
            max_connections=data.get('max_connections'),
            allowed_updates=data.get('allowed_updates')
        )

    def __repr__(self):
        return f"<WebhookInfo url={self.url}, has_custom_certificate={self.has_custom_certificate}, " \
               f"pending_update_count={self.pending_update_count}, last_error_date={self.last_error_date}, " \
               f"last_error_message={self.last_error_message}, max_connections={self.max_connections}, " \
               f"allowed_updates={self.allowed_updates}>"


class InputFile:
    def __init__(self, file_path):
        self.file_path = file_path

    def __str__(self):
        return self.file_path


class InputMediaPhoto:
    def __init__(self, media, caption=None):
        self.type = 'photo'
        self.media = media
        self.caption = caption

    def to_dict(self):
        data = {'type': self.type, 'media': self.media}
        if self.caption:
            data['caption'] = self.caption
        return data


class InputMediaAnimation:
    def __init__(self, media, caption=None, duration=None, width=None, height=None):
        self.type = 'animation'
        self.media = media
        self.caption = caption
        self.duration = duration
        self.width = width
        self.height = height

    def to_dict(self):
        payload = {'type': self.type, 'media': self.media}
        if self.caption:
            payload['caption'] = self.caption
        if self.duration:
            payload['duration'] = self.duration
        if self.width:
            payload['width'] = self.width
        if self.height:
            payload['height'] = self.height
        return payload


class InputMediaVideo:
    def __init__(self, media, caption=None, duration=None, width=None, height=None, supports_streaming=False):
        self.type = 'video'
        self.media = media
        self.caption = caption
        self.duration = duration
        self.width = width
        self.height = height
        self.supports_streaming = supports_streaming

    def to_dict(self):
        payload = {'type': self.type, 'media': self.media}
        if self.caption:
            payload['caption'] = self.caption
        if self.duration:
            payload['duration'] = self.duration
        if self.width:
            payload['width'] = self.width
        if self.height:
            payload['height'] = self.height
        payload['supports_streaming'] = self.supports_streaming
        return payload


class CallbackQuery:
    def __init__(self, callback_query_data):
        self.id = callback_query_data['id']
        self.from_user = User.from_dict(callback_query_data['from'])
        self.data = callback_query_data.get('data')
        self.message = Message.from_dict(callback_query_data['message'])
        self.inline_message_id = callback_query_data.get('inline_message_id')
        self.chat_instance = callback_query_data.get('chat_instance')
        self.game_short_name = callback_query_data.get('game_short_name')


class Message:
    def __init__(self, message_id, chat, from_user, text=None, date=None, 
                 reply_to_message=None, content_type=None, photo=None, 
                 audio=None, video=None, video_note=None, voice=None, 
                 animation=None, dice=None, sticker=None, document=None, 
                 new_chat_members=None, new_chat_member=None, left_chat_member=None):
        self.message_id = message_id
        self.chat = chat
        self.from_user = from_user
        self.text = text
        self.date = date
        self.reply_to_message = reply_to_message
        self.content_type = content_type
        self.photo = photo
        self.audio = audio
        self.video = video
        self.video_note = video_note
        self.voice = voice
        self.animation = animation
        self.dice = dice
        self.sticker = sticker
        self.document = document
        self.new_chat_members = new_chat_members
        self.new_chat_member = new_chat_member
        self.left_chat_member = left_chat_member

    @classmethod
    def from_dict(cls, data):
        chat = Chat.from_dict(data['chat'])
        from_user = User.from_dict(data['from']) if 'from' in data else None
        reply_to_message = Message.from_dict(data['reply_to_message']) if 'reply_to_message' in data else None
        content_type = None
        photo = None
        audio = None
        video = None
        video_note = None
        voice = None
        animation = None
        dice = None
        sticker = None
        document = None
        new_chat_members = None
        new_chat_member = None
        left_chat_member = None
        text = None
        if 'text' in data:
            content_type = 'text'
            text = data.get('text')
        elif 'photo' in data:
            content_type = 'photo'
            photo = [Photo.from_dict(p) for p in data['photo']]
        elif 'audio' in data:
            content_type = 'audio'
            audio = Audio.from_dict(data['audio'])
        elif 'video' in data:
            content_type = 'video'
            video = Video.from_dict(data['video'])
        elif 'video_note' in data:
            content_type = 'video_note'
            video_note = VideoNote.from_dict(data['video_note'])
        elif 'voice' in data:
            content_type = 'voice'
            voice = Voice.from_dict(data['voice'])
        elif 'animation' in data:
            content_type = 'animation'
            animation = Animation.from_dict(data['animation'])
        elif 'dice' in data:
            content_type = 'dice'
            dice = Dice.from_dict(data['dice'])
        elif 'sticker' in data:
            content_type = 'sticker'
            sticker = Sticker.from_dict(data['sticker'])
        elif 'document' in data:
            content_type = 'document'
            document = Document.from_dict(data['document'])
        elif 'new_chat_members' in data:
            content_type = 'new_chat_members'
            new_chat_members = [User.from_dict(member) for member in data['new_chat_members']]
        elif 'new_chat_member' in data:
            content_type = 'new_chat_member'
            new_chat_member = User.from_dict(data['new_chat_member'])
        elif 'left_chat_member' in data:
            content_type = 'left_chat_member'
            left_chat_member = User.from_dict(data['left_chat_member'])
        return cls(
            message_id=data['message_id'],
            chat=chat,
            from_user=from_user,
            text=text,
            date=data.get('date'),
            reply_to_message=reply_to_message,
            content_type=content_type,
            photo=photo,
            audio=audio,
            video=video,
            video_note=video_note,
            voice=voice,
            animation=animation,
            dice=dice,
            sticker=sticker,
            document=document,
            new_chat_members=new_chat_members,
            new_chat_member=new_chat_member,
            left_chat_member=left_chat_member
        )

    def __repr__(self):
        return (f"Message(message_id={self.message_id}, text={self.text}, "
                f"content_type={self.content_type}, photo={self.photo}, "
                f"audio={self.audio}, video={self.video}, "
                f"video_note={self.video_note}, voice={self.voice}, "
                f"animation={self.animation}, dice={self.dice}, "
                f"document={self.document}, new_chat_members={self.new_chat_members}, "
                f"new_chat_member={self.new_chat_member}, left_chat_member={self.left_chat_member})")


#Основа
class Bot:
    def __init__(self, token):
        self.token = token
        self.handlers = {'message': [], 'command': [], 'callback_query': []}
        self.running = False
        self.update_offset = 0
        self.next_steps = {}

    def _make_request(self, method, params=None, files=None, json=None):
        '''Отправляет запрос в Telegram API'''
        url = f'https://api.telegram.org/bot{self.token}/{method}'
        response = requests.post(url, params=params, files=files, json=json)
        if response.status_code != 200:
            print(f"Ошибка: {response.status_code} - {response.text}")
            return None
        return response.json()

    def reply_message(self, chat_id, text, mode="Markdown", disable_web_page_preview=None, disable_notification=None, reply_to_message_id=None, reply_markup=None):
        '''Отправляет сообщение'''
        method = 'sendMessage'
        if not chat_id and not text:
            raise ValueError("chat_id и text не должны быть None")
        params = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': mode,
            'disable_web_page_preview': disable_web_page_preview,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        if reply_markup is not None:
            params['reply_markup'] = json.dumps(reply_markup)
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None

    def reply_photo(self, chat_id, photo, caption=None, mode="Markdown", disable_notification=None, reply_to_message_id=None, reply_markup=None):
        '''Отправляет фото'''
        method = 'sendPhoto'
        if not chat_id and not photo:
            raise ValueError("chat_id и photo не должны быть None")
        params = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': mode,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        if reply_markup is not None:
            params['reply_markup'] = json.dumps(reply_markup)
        if isinstance(photo, str):
            params['photo'] = photo
            files = None
        else:
            files = {'photo': photo}
        response = self._make_request(method, params, files)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None

    def reply_audio(self, chat_id, audio, caption=None, mode="Markdown", duration=None, performer=None, title=None, thumb=None, disable_notification=None, reply_to_message_id=None, reply_markup=None):
        '''Отправляет аудио'''
        method = 'sendAudio'
        if not chat_id and not audio:
            raise ValueError("chat_id и audio не должны быть None")
        params = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': mode,
            'duration': duration,
            'performer': performer,
            'title': title,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        if reply_markup is not None:
            params['reply_markup'] = json.dumps(reply_markup)
        if isinstance(audio, str):
            params['audio'] = audio
            files = None
        else:
            files = {'audio': audio}
        if thumb is not None:
            if isinstance(thumb, str):
                params['thumb'] = thumb
            else:
                files['thumb'] = thumb
        response = self._make_request(method, params, files)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None

    def reply_document(self, chat_id, document, caption=None, mode="Markdown", disable_notification=None, reply_to_message_id=None, reply_markup=None):
        '''Отправляет документ'''
        if not chat_id and not document:
            raise ValueError("chat_id и document не должны быть None")
        method = 'sendDocument'
        params = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': mode,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        if reply_markup is not None:
            params['reply_markup'] = json.dumps(reply_markup)
        if isinstance(document, str):
            params['document'] = document
            files = None
        else:
            files = {'document': document}
        response = self._make_request(method, params, files)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None

    def reply_video(self, chat_id, video, duration=None, width=None, height=None, caption=None, mode="Markdown", supports_streaming=None, disable_notification=None, reply_to_message_id=None, reply_markup=None):
        '''Отправляет видео'''
        method = 'sendVideo'
        if not chat_id and not video:
            raise ValueError("chat_id и video не должны быть None")
        params = {
            'chat_id': chat_id,
            'duration': duration,
            'width': width,
            'height': height,
            'caption': caption,
            'parse_mode': mode,
            'supports_streaming': supports_streaming,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        if reply_markup is not None:
            params['reply_markup'] = json.dumps(reply_markup)
        if isinstance(video, str):
            params['video'] = video
            files = None
        else:
            files = {'video': video}
        response = self._make_request(method, params, files)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None
    
    def reply_video_note(self, chat_id, video_note, duration=None, length=None, disable_notification=None, reply_to_message_id=None, reply_markup=None):
        '''Отправляет видео кружочек'''
        method = 'sendVideoNote'
        if not chat_id and not video_note:
            raise ValueError("chat_id и video_note не должны быть None")
        params = {
            'chat_id': chat_id,
            'duration': duration,
            'length': length,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        if reply_markup is not None:
            params['reply_markup'] = json.dumps(reply_markup)
        if isinstance(video_note, str):
            params['video_note'] = video_note
            files = None
        else:
            files = {'video_note': video_note}
        response = self._make_request(method, params, files)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None

    def reply_animation(self, chat_id, animation, duration=None, width=None, height=None, caption=None, mode="Markdown", disable_notification=None, reply_to_message_id=None, reply_markup=None):
        '''Отправляет анимацию'''
        method = 'sendAnimation'
        if not chat_id and not animation:
            raise ValueError("chat_id и animation не должны быть None")
        params = {
            'chat_id': chat_id,
            'duration': duration,
            'width': width,
            'height': height,
            'caption': caption,
            'parse_mode': mode,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        if reply_markup is not None:
            params['reply_markup'] = json.dumps(reply_markup)
        if isinstance(animation, str):
            params['animation'] = animation
            files = None
        else:
            files = {'animation': animation}
        response = self._make_request(method, params, files)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None

    def reply_voice(self, chat_id, voice, caption=None, mode="Markdown", duration=None, disable_notification=None, reply_to_message_id=None, reply_markup=None):
        '''Отправляет голосовое сообщение'''
        method = 'sendVoice'
        if not chat_id and not voice:
            raise ValueError("chat_id и voice не должны быть None")
        params = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': mode,
            'duration': duration,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        if reply_markup is not None:
            params['reply_markup'] = json.dumps(reply_markup)
        if isinstance(voice, str):
            params['voice'] = voice
            files = None
        else:
            files = {'voice': voice}
        response = self._make_request(method, params, files)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None

    def reply_location(self, chat_id, latitude, longitude, live_period=None, disable_notification=None, reply_to_message_id=None, reply_markup=None):
        '''Отправляет локацию в chat_id'''
        method = 'sendLocation'
        if not chat_id and not latitude and not longitude:
            raise ValueError("chat_id и latitude и longitude не должны быть None")
        params = {
            'chat_id': chat_id,
            'latitude': latitude,
            'longitude': longitude,
            'live_period': live_period,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        if reply_markup is not None:
            params['reply_markup'] = json.dumps(reply_markup)
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None

    def reply_chat_action(self, chat_id, action):
        '''Отправляет активность'''
        method = 'sendChatAction'
        if not chat_id and not action:
            raise ValueError("chat_id и action не должны быть None")
        params = {'chat_id': chat_id, 'action': action}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return response['result']
        else:
            print(f"Ошибка: {response}")
            return None
    
    def reply_venue(self, chat_id, latitude, longitude, title, address, foursquare_id=None, disable_notification=None, reply_to_message_id=None, reply_markup=None):
        '''Отправляет место (venue) в chat_id'''
        method = 'sendVenue'
        if not chat_id and not latitude and not longitude and not title and not address:
            raise ValueError("chat_id и latitude и longitude не должны быть None")
        params = {
            'chat_id': chat_id,
            'latitude': latitude,
            'longitude': longitude,
            'title': title,
            'address': address,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        if reply_markup is not None:
            params['reply_markup'] = json.dumps(reply_markup)
        if foursquare_id:
            params['foursquare_id'] = foursquare_id
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None
    
    def reply_contact(self, chat_id, phone_number, first_name, last_name=None, disable_notification=None, reply_to_message_id=None, reply_markup=None):
        '''Отправляет контакт в chat_id'''
        method = 'sendContact'
        if not chat_id and not phone_number and not first_name:
            raise ValueError("chat_id и phone_number и first_name не должны быть None")
        params = {
            'chat_id': chat_id,
            'phone_number': phone_number,
            'first_name': first_name,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        if reply_markup is not None:
            params['reply_markup'] = json.dumps(reply_markup)
        if last_name:
            params['last_name'] = last_name
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None
    
    def reply_sticker(self, chat_id, sticker, disable_notification=None, reply_to_message_id=None, reply_markup=None):
        '''Отправляет стикер в chat_id'''
        method = 'sendSticker'
        if not chat_id and not sticker:
            raise ValueError("chat_id и sticker не должны быть None")
        params = {
            'chat_id': chat_id,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        if reply_markup is not None:
            params['reply_markup'] = json.dumps(reply_markup)
        if isinstance(sticker, str):
            params['sticker'] = sticker
            files = None
        else:
            files = {'sticker': sticker}
        response = self._make_request(method, params, files)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None
        
    def reply_dice(self, chat_id, emoji, disable_notification=None, reply_to_message_id=None, reply_markup=None):
        '''Отправляет анимированные эмодзи в chat_id'''
        method = 'sendDice'
        if not chat_id and not emoji:
            raise ValueError("chat_id и emoji не должны быть None")
        params = {
            'chat_id': chat_id,
            'emoji': emoji,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        if reply_markup is not None:
            params['reply_markup'] = json.dumps(reply_markup)
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None

    def reply_message_reaction(self, chat_id, message_id, reaction=['👍'], is_big=False):
        '''Отправить реакцию'''
        method = 'setMessageReaction'
        if not chat_id and not message_id and not reaction:
            raise ValueError("chat_id и message_id и reaction не должны быть None")
        payload = {
            'chat_id': chat_id,
            'message_id': message_id,
            'reaction': [{'type': 'emoji', 'emoji': dict(reaction)}],
            'is_big': is_big
        }
        response = self._make_request(method, json=payload)
        if response and 'result' in response:
            return True
        else:
            print(f"Ошибка: {response}")
            return False

    def reply_poll(self, chat_id, question, options, disable_notification=None, reply_to_message_id=None, reply_markup=None):
        '''Отправляет опрос в chat_id'''
        method = 'sendPoll'
        if not chat_id and not question and not options:
            raise ValueError("chat_id и question и options не должны быть None")
        params = {
            'chat_id': chat_id,
            'question': question,
            'options': json.dumps(options),
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        if reply_markup is not None:
            params['reply_markup'] = json.dumps(reply_markup)
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            print(f"Ошибка: {response}")
            return False
    
    def stop_poll(self, chat_id, message_id, reply_markup=None):
        '''Завершает активный опрос в чате'''
        method = 'stopPoll'
        if not chat_id or not message_id:
            raise ValueError("chat_id и message_id не могут быть None")
        params = {'chat_id': chat_id, 'message_id': message_id}
        if reply_markup is not None:
            params['reply_markup'] = json.dumps(reply_markup)
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            print(f"Ошибка: {response}")
            return False
        
    def pin_message(self, chat_id, message_id):
        '''Закрепляет сообщение в чате'''
        method = 'pinChatMessage'
        if not chat_id and not message_id:
            raise ValueError("chat_id и message_id не могут быть None")
        params = {'chat_id': chat_id, 'message_id': message_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            print(f"Ошибка: {response}")
            return False

    def unpin_message(self, chat_id, message_id):
        '''Открепляет сообщение в чате'''
        method = 'unpinChatMessage'
        if not chat_id and not message_id:
            raise ValueError("chat_id и message_id не могут быть None")
        params = {'chat_id': chat_id, 'message_id': message_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            print(f"Ошибка: {response}")
            return False

    def forward_message(self, chat_id, from_chat_id, message_id, disable_notification=None):
        '''Пересылает сообщение'''
        method = 'forwardMessage'
        if not chat_id and not from_chat_id and not message_id:
            raise ValueError("chat_id, from_chat_id и message_id не должны быть None")
        params = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'message_id': message_id,
            'disable_notification': disable_notification
        }
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None
    
    def forward_messages(self, chat_id, from_chat_id, message_ids, disable_notification=None):
        '''Пересылает несколько сообщений'''
        method = 'forwardMessages'
        if not chat_id and not from_chat_id and not message_ids:
            raise ValueError("chat_id, from_chat_id и message_ids не должны быть None")
        params = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'message_ids': message_ids,
            'disable_notification': disable_notification
        }
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None

    def copy_message(self, chat_id, from_chat_id, message_id, caption=None, disable_notification=None, mode="Markdown", reply_markup=None):
        '''Копирует сообщение'''
        method = 'copyMessage'
        if not chat_id and not from_chat_id and not message_id:
            raise ValueError("chat_id, from_chat_id и message_id не должны быть None")
        params = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'message_id': message_id,
            'caption': caption,
            'parse_mode': mode,
            'disable_notification': disable_notification
        }
        if  reply_markup is not None:
            params['reply_markup'] = json.dumps(reply_markup)
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None
    
    def copy_messages(self, chat_id, from_chat_id, message_ids, disable_notification=None):
        '''Копирует несколько сообщений'''
        method = 'copyMessages'
        if not chat_id and not from_chat_id and not message_ids:
            raise ValueError("chat_id, from_chat_id и message_ids не должны быть None")
        params = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'message_ids': message_ids,
            'disable_notification': disable_notification
        }
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None

    def delete_message(self, chat_id, message_id):
        '''Удаляет сообщение'''
        method = 'deleteMessage'
        if not chat_id and not message_id:
            raise ValueError("chat_id и message_id не должны быть None")
        params = {
            'chat_id': chat_id,
            'message_id': message_id
        }
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None

    def delete_messages(self, chat_id, message_ids):
        '''Удаляет все сообщения'''
        if not chat_id and not message_ids:
            raise ValueError("chat_id и message_ids не должны быть None")
        for message_id in message_ids:
            self.delete_message(chat_id, message_id)

    def get_user_profile_photos(self, user_id, offset=None, limit=None, photo_index=None):
        '''Получает список фотографий пользователя и возвращает указанные фото или весь список file_id'''
        method_url = 'getUserProfilePhotos'
        if not user_id:
            raise ValueError("user_id не должен быть None")
        payload = {
            'user_id': user_id,
            'offset': offset,
            'limit': limit
        }
        response = self._make_request(method_url, params=payload)
        if 'result' in response:
            photos = response['result']['photos']
            if photos:
                if photo_index is not None and 0 <= photo_index < len(photos):
                    selected_photo = photos[photo_index][-1]
                    return selected_photo['file_id']
                else:
                    return [photo[-1]['file_id'] for photo in photos]
            else:
                return None
        else:
            return None
    
    def get_me(self):
        '''Возвращает объект бота'''
        method = 'getMe'
        response = self._make_request(method)
        if 'result' in response:
            return User.from_dict(response['result'])
        else:
            print(f"Error getting bot info: {response}")
            return None

    def get_file(self, file_id):
        '''Получает информацию о файле на серверах Telegram'''
        method = 'getFile'
        if not file_id:
            raise ValueError("file_id не может быть None")
        params = {'file_id': file_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return File.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None

    def download_file(self, file, save_path, chunk_size=1024, timeout=60, headers=None, stream=True):
        '''Скачивает файл с серверов Telegram и сохраняет на диск'''
        if not isinstance(file, File):
            raise ValueError("file должен быть объектом класса TelegramFile")
        if not file.file_path and not save_path:
            raise ValueError("file_path и save_path не должны быть None")
        if not os.path.isdir(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
        file_url = f"https://api.telegram.org/file/bot{self.token}/{file.file_path}"
        try:
            with requests.get(file_url, stream=stream, timeout=timeout, headers=headers) as response:
                if response.status_code == 200:
                    with open(save_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            f.write(chunk)
                    return True
                else:
                    print(f"Ошибка при скачивании файла: {response.status_code} - {response.text}")
                    return False
        except requests.exceptions.RequestException as e:
            print(f"Произошла ошибка при скачивании файла: {e}")

#Редакт чего-то
    def edit_message_text(self, chat_id, message_id, text, inline_message_id=None, mode="Markdown", reply_markup=None):
        '''Редактирует текст сообщения'''
        method = 'editMessageText'
        if not chat_id and not message_id and not text:
            raise ValueError("chat_id, message_id и text не должны быть None")
        params = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text,
            'parse_mode': mode
        }
        if inline_message_id is not None:
            params['inline_message_id'] = inline_message_id
        if reply_markup is not None:
            params['reply_markup'] = json.dumps(reply_markup)
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None

    def edit_message_caption(self, chat_id, message_id, caption, mode="Markdown", inline_message_id=None, show_caption_above_media=False, reply_markup=None):
        '''Редактирует описание медиа'''
        method = 'editMessageCaption'
        if not chat_id and not message_id and not caption:
            raise ValueError("chat_id, message_id и caption не должны быть None")
        params = {
            'chat_id': chat_id,
            'message_id': message_id,
            'caption': caption,
            'parse_mode': mode,
            }
        if inline_message_id is not None:
            params['inline_message_id'] = inline_message_id
        if show_caption_above_media is not None:
            params['show_caption_above_media'] = show_caption_above_media
        if reply_markup is not None:
            params['reply_markup'] = json.dumps(reply_markup)
        response = self._make_request(method, params)
        if response and 'result' in response:
            return response['result']
        else:
            print(f"Ошибка: {response}")
            return None

    def edit_message_media(self, chat_id, message_id, media, caption=None, inline_message_id=None, reply_markup=None):
        '''Редактирует медиа контент в сообщении'''
        method = 'editMessageMedia'
        if not chat_id and not message_id and not media:
            raise ValueError("chat_id, message_id и media не должны быть None")
        if isinstance(media, InputMediaPhoto):
            media_payload = media.to_dict()
        elif isinstance(media, InputMediaAnimation):
            media_payload = media.to_dict()
        elif isinstance(media, InputMediaVideo):
            media_payload = media.to_dict()
        elif isinstance(media, str):
            media_payload = {'type': 'photo', 'media': media}
        else:
            raise ValueError('media должно быть экземпляром InputMediaPhoto, InputMediaAnimation или InputMediaVideo')
        params = {'media': media_payload}
        if caption is not None:
            params['caption'] = caption
        if inline_message_id is not None:
            params['inline_message_id'] = inline_message_id
        if reply_markup is not None:
            params['reply_markup'] = json.dumps(reply_markup)
        response = self._make_request(method, json=params)
        if response and 'result' in response:
            return response['result']
        else:
            print(f"Ошибка: {response}")
            return None

    def edit_message_reply_markup(self, chat_id, message_id, reply_markup, inline_message_id=None, ):
        '''Редактирует клавиатуру сообщения'''
        method = 'editMessageReplyMarkup'
        if not chat_id and message_id and reply_markup:
            raise ValueError("chat_id, message_id и reply_markup не должны быть None")
        params = {
            'chat_id': chat_id,
            'message_id': message_id,
            'reply_markup': json.dumps(reply_markup)
        }
        if inline_message_id:
            params['inline_message_id'] = inline_message_id
        response = self._make_request(method, params)
        if response and 'result' in response:
            return response['result']
        else:
            print(f"Ошибка: {response}")
            return None

#Вэбхук    
    def set_webhook(self, url, certificate=None, max_connections=None, allowed_updates=None):
        '''Устанавливает вебхук'''
        method = 'setWebhook'
        if not url:
            raise ValueError("url не может быть None")
        params = {
            'url': url,
            'max_connections': max_connections,
            'allowed_updates': json.dumps(allowed_updates) if allowed_updates else None
        }
        files = {'certificate': certificate} if certificate else None
        response = self._make_request(method, params, files)
        if response and 'result' in response:
            return WebhookInfo.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None

    def get_webhook_info(self, timeout=30, drop_pending_updates=None):
        '''Получает информацию о текущем webhook.'''
        method = 'getWebhookInfo'
        payload = {}
        if timeout:
            payload['timeout'] = timeout
        if drop_pending_updates is not None:
            payload['drop_pending_updates'] = drop_pending_updates
        response = self._make_request(method, params=payload)
        if response and 'result' in response:
            return WebhookInfo.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None
    
    def delete_webhook(self, drop_pending_updates=False):
        '''Удаляет вебхук'''
        method = 'deleteWebhook'
        payload = {'drop_pending_updates': drop_pending_updates}
        response = self._make_request(method, params=payload)
        if response and 'result' in response:
            return response['result']
        else:
            print(f"Ошибка: {response}")
            return None

#Получение апдейтов
    def get_updates(self, timeout=20, allowed_updates=None, long_polling_timeout=30):
        '''Запрос обновлений с учетом дополнительных параметров'''
        method = 'getUpdates'
        params = {'timeout': timeout, 'allowed_updates': allowed_updates}
        if self.update_offset:
            params['offset'] = self.update_offset
        if long_polling_timeout:
            params['long_polling_timeout'] = long_polling_timeout
        updates = self._make_request(method, params)
        if updates and 'result' in updates:
            return updates['result']
        return []

    def process_updates(self, updates):
        '''Обрабатывает полученные обновления'''
        if not updates:
            raise ValueError("updates не должны быть None")
        for update in updates:
            if 'message' in update:
                self._handle_message(update['message'])
                self.update_offset = update['update_id'] + 1
            elif 'callback_query' in update:
                self._handle_callback_query(update['callback_query'])
                self.update_offset = update['update_id'] + 1
    
    def polling(self, interval=1):
        '''Передает обновления в течение длительного промежутка времени'''
        self.running = True
        while self.running:
            updates = self.get_updates()
            if updates:
                self.process_updates(updates)
            time.sleep(interval)

    def always_polling(self, interval=1, timeout=20, long_polling_timeout=30, allowed_updates=None, restart_on_error=True):
        '''Продолжает работу бесконечно, игнорируя ошибки и поддерживает параметры управления'''
        self.running = True
        while self.running:
            try:
                updates = self.get_updates(timeout=timeout, allowed_updates=allowed_updates, long_polling_timeout=long_polling_timeout)
                if updates:
                    self.process_updates(updates)
            except Exception as e:
                print(f"Ошибка: {e}")
                if not restart_on_error:
                    self.running = False
            time.sleep(interval)

    def stop_polling(self):
        '''Останавливает получение обновлений'''
        self.running = False

#Чат инфа
    def get_chat(self, chat_id):
        '''Получает информацию о чате'''
        method = 'getChat'
        if not chat_id:
            raise ValueError("chat_id не может быть None")
        params = {'chat_id': chat_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Chat.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None

    def get_chat_administrators(self, chat_id):
        '''Получает список администраторов чата'''
        method = 'getChatAdministrators'
        if not chat_id:
            raise ValueError("chat_id не может быть None")
        params = {'chat_id': chat_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return response['result']
        else:
            print(f"Ошибка: {response}")
            return []

    def get_chat_members_count(self, chat_id):
        '''Получает количество участников чата'''
        method = 'getChatMembersCount'
        if not chat_id:
            raise ValueError("chat_id не может быть None")
        params = {'chat_id': chat_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return response['result']
        else:
            print(f"Ошибка: {response}")
            return 0

    def get_chat_member(self, chat_id, user_id):
        '''Получает информацию о пользователе чата'''
        method = 'getChatMember'
        if not chat_id and not user_id:
            raise ValueError("chat_id и user_id не могут быть None")
        params = {'chat_id': chat_id, 'user_id': user_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return User.from_dict(response['result']['user'])
        else:
            print(f"Ошибка: {response}")
            return None

    def set_chat_photo(self, chat_id, photo):
        '''Устанавливает фото для чата'''
        method = 'setChatPhoto'
        files = None
        if not chat_id and not photo:
            raise ValueError("chat_id и photo не могут быть None")
        if isinstance(photo, InputFile):
            params = {'chat_id': chat_id}
            files = {'photo': open(photo.file_path, 'rb')}
        elif isinstance(photo, str):
            if photo.startswith('http'):
                params = {'chat_id': chat_id, 'photo': photo}
            else:
                params = {'chat_id': chat_id}
                files = {'photo': open(photo, 'rb')}
        else:
            raise ValueError("Неверный формат фото. Ожидается InputFile, путь к файлу, file_id или URL.")
        response = self._make_request(method, params, files)
        if files:
            files['photo'].close()
        if response and 'result' in response:
            return True
        else:
            print(f"Ошибка: {response}")
            return False

    def delete_chat_photo(self, chat_id):
        '''Удаляет фотографию чата'''
        method = 'deleteChatPhoto'
        if not chat_id:
            raise ValueError("chat_id не может быть None")
        params = {'chat_id': chat_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            print(f"Ошибка: {response}")
            return False

    def set_chat_title(self, chat_id, title):
        '''Устанавливает название чата'''
        method = 'setChatTitle'
        if not chat_id and not title:
            raise ValueError("chat_id и title не могут быть None")
        params = {'chat_id': chat_id, 'title': title}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            print(f"Ошибка: {response}")
            return None
        
    def set_chat_description(self, chat_id, description):
        '''Устанавливает описание для чата'''
        method = 'setChatDescription'
        if not chat_id or not description:
            raise ValueError("chat_id и description не могут быть None")
        params = {'chat_id': chat_id, 'description': description}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            print(f"Ошибка: {response}")
            return False

    def leave_chat(self, chat_id):
        '''Покидает чат'''
        method = 'leaveChat'
        if not chat_id:
            raise ValueError("chat_id не может быть None")
        params = {'chat_id': chat_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            print(f"Ошибка: {response}")
            return False
    
# Административные команды
    def kick_chat_member(self, chat_id, user_id, until_date=time.time()):
        '''Выгоняет пользователя из чата'''
        method = 'kickChatMember'
        if not chat_id and not user_id:
            raise ValueError("chat_id и user_id не могут быть None")
        params = {'chat_id': chat_id, 'user_id': user_id, 'until_date': until_date}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            print(f"Ошибка: {response}")
            return False

    def ban_chat_member(self, chat_id, user_id, until_date=time.time(), revoke_messages=False):
        '''Блокирует пользователя в чате'''
        method = 'banChatMember'
        if not chat_id and not user_id:
            raise ValueError("chat_id и user_id не могут быть None")
        params = {
            'chat_id': chat_id,
            'user_id': user_id,
            'until_date': until_date,
            'revoke_messages': revoke_messages
        }
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            print(f"Ошибка: {response}")
            return False

    def unban_chat_member(self, chat_id, user_id, only_if_banned=False):
        '''Разблокирует пользователя в чате'''
        method = 'unbanChatMember'
        if not chat_id and not user_id:
            raise ValueError("chat_id и user_id не могут быть None")
        params = {'chat_id': chat_id, 'user_id': user_id, 'only_if_banned': only_if_banned}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            print(f"Ошибка: {response}")
            return False
    
    def mute_user(self, chat_id, user_id, duration=3600):
        '''Заблокирует отправку сообщений для пользователя в чате'''
        method = 'restrictChatMember'
        if not chat_id and not user_id:
            raise ValueError("chat_id и user_id не могут быть None")
        params = {
            'chat_id': chat_id,
            'user_id': user_id,
            'permissions': {
                'can_send_messages': False,
                'can_send_media_messages': False,
                'can_send_other_messages': False,
                'can_invite_to_chats': False,
                'can_pin_messages': False,
                'can_change_info': False
            }
        }
        if duration:
            until_date = time.time() + duration
            params['until_date'] = until_date
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            print(f"Ошибка: {response}")
            return False

    def unmute_user(self, chat_id, user_id):
        '''Разблокирует отправку сообщений для пользователя в чате'''
        method = 'restrictChatMember'
        if not chat_id and not user_id:
            raise ValueError("chat_id и user_id не могут быть None")
        params = {
            'chat_id': chat_id,
            'user_id': user_id,
            'permissions': {
                'can_send_messages': True,
                'can_send_media_messages': True,
                'can_send_other_messages': True,
                'can_invite_to_chats': True,
                'can_pin_messages': True,
                'can_change_info': True
            }
        }
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            print(f"Ошибка: {response}")
            return False

    def restrict_chat_member(self, chat_id, user_id, permissions, until_date=time.time()):
        '''Изменяет разрешения пользователя в чате'''
        method = 'restrictChatMember'
        if not chat_id and not user_id and not permissions:
            raise ValueError("chat_id, user_id и permissions не могут быть None")
        params = {
            'chat_id': chat_id,
            'user_id': user_id,
            'permissions': permissions,
            'until_date': until_date
        }
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            print(f"Ошибка: {response}")
            return False

    def promote_chat_member(self, chat_id, user_id, can_change_info=False, can_post_messages=False,
                            can_edit_messages=False, can_delete_messages=False, can_invite_users=False,
                            can_restrict_members=False, can_pin_messages=False, can_promote_members=False):
        '''Изменяет права пользователя в чате'''
        method = 'promoteChatMember'
        if not chat_id and not user_id:
            raise ValueError("chat_id и user_id не могут быть None")
        params = {
            'chat_id': chat_id,
            'user_id': user_id,
            'can_change_info': can_change_info,
            'can_post_messages': can_post_messages,
            'can_edit_messages': can_edit_messages,
            'can_delete_messages': can_delete_messages,
            'can_invite_users': can_invite_users,
            'can_restrict_members': can_restrict_members,
            'can_pin_messages': can_pin_messages,
            'can_promote_members': can_promote_members
        }
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            print(f"Ошибка: {response}")
            return False

    def set_chat_permissions(self, chat_id, permissions):
        '''Проверка прав пользователя в чате'''
        method = 'setChatPermissions'
        if not chat_id and not permissions:
            raise ValueError("chat_id и permissions не могут быть None")
        params = {'chat_id': chat_id, 'permissions': permissions}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return response['result']
        else:
            print(f"Ошибка: {response}")
            return None
    
    def chat_permissions(self, can_send_messages=True, can_send_media_messages=True,
                     can_send_polls=True, can_send_other_messages=True, can_add_web_page_previews=True,
                     can_change_info=False, can_invite_users=True, can_pin_messages=False):
        '''Установка прав пользователя в чате'''
        permissions = {
            'can_send_messages': can_send_messages,
            'can_send_media_messages': can_send_media_messages,
            'can_send_polls': can_send_polls,
            'can_send_other_messages': can_send_other_messages,
            'can_add_web_page_previews': can_add_web_page_previews,
            'can_change_info': can_change_info,
            'can_invite_users': can_invite_users,
            'can_pin_messages': can_pin_messages
        }
        return json.dumps(permissions)

#Регистрация хэндлеров
    def message_handler(self, func=None, commands=None, regexp=None, content_types=None):
        '''Регистрирует все сообщения разных типов'''
        def decorator(handler):
            self.handlers['message'].append({
                'function': handler,
                'func': func,
                'commands': commands,
                'regexp': re.compile(regexp) if regexp else None,
                'content_types': content_types
            })
            return handler
        return decorator

    def _handle_message(self, message_data):
        '''Обработка сообщений'''
        if not message_data:
            raise ValueError("message_data не должно быть None")
        message = Message.from_dict(message_data)
        chat_id = message.chat.id
        if chat_id in self.next_steps:
            step = self.next_steps[chat_id]
            step['callback'](message, *step['args'], **step['kwargs'])
            del self.next_steps[chat_id]
            return
        text = str(message.text)
        if text and text.startswith('/'):
            command = text.split()[0][1:].lower()
            for handler in self.handlers['message']:
                if handler['commands'] and command in handler['commands']:
                    if handler['func'] is None or handler['func'](message):
                        handler['function'](message)
                        return
        for handler in self.handlers['message']:
            if handler['regexp'] and handler['regexp'].search(text):
                if handler['func'] is None or handler['func'](message):
                    handler['function'](message)
                    return
        for handler in self.handlers['message']:
            if not handler['regexp'] and not handler['commands']:
                if handler['content_types']:
                    if message.content_type in handler['content_types']:
                        if handler['func'] is None or handler['func'](message):
                            handler['function'](message)
                            return
                else:
                    if handler['func'] is None or handler['func'](message):
                        handler['function'](message)
                        return

    def register_next_step_handler(self, message, callback, *args, **kwargs):
        '''Регистрирует следующий обработчик для сообщения'''
        if not message and not callback:
            raise ValueError("message или callback не должны быть None")
        chat_id = message.chat.id
        self.next_steps[chat_id] = {'callback': callback, 'args': args, 'kwargs': kwargs}

    def callback_query_handler(self, func=None, data=None):
        '''Регистрирует callback запросы'''
        def decorator(handler):
            self.handlers['callback_query'].append({
                'function': handler,
                'func': func,
                'data': data
            })
            return handler
        return decorator

    def _handle_callback_query(self, callback_query_data):
        '''Обрабатывает нажатия на инлайн-кнопки'''
        if not callback_query_data:
            raise ValueError("callback_query_data не должно быть None")
        callback_query = CallbackQuery(callback_query_data)
        data = callback_query.data
        for handler in self.handlers['callback_query']:
            if handler['data'] is None or handler['data'] == data:
                if handler['func'] is None or handler['func'](callback_query):
                    handler['function'](callback_query)
                    break

    def answer_callback_query(self, callback_id, text="Something has been forgotten", show_alert=False, url=None, cache_time=0):
        '''Отвечает на запрос callback'''
        method = 'answerCallbackQuery'
        if not callback_id:
            raise ValueError("callback_id не должен быть None")
        params = {
            'callback_query_id': callback_id,
            'text': text,
            'show_alert': show_alert,
            'cache_time': cache_time
        }
        if url is not None:
            params['url'] = url
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            print(f"Ошибка: {response}")
            return False


#Кнопки
class Markup:
    @staticmethod
    def create_reply_keyboard(buttons, row_width=2):
        keyboard = []
        for i in range(0, len(buttons), row_width):
            keyboard.append(buttons[i:i + row_width])
        return {'keyboard': keyboard, 'resize_keyboard': True, 'one_time_keyboard': True}

    @staticmethod
    def check_reply_keyboard(check=True):
        '''Удаляет/Показывает обычную клавиатуры'''
        return {'remove_keyboard': check}

    @staticmethod
    def create_inline_keyboard(buttons, row_width=2):
        keyboard = []
        for i in range(0, len(buttons), row_width):
            keyboard.append(buttons[i:i + row_width])
        return {'inline_keyboard': keyboard}
