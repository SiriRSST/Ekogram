import requests, json, os, time, re, random
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from typing import Optional, Union


class User:
    def __init__(self, user_id: int, is_bot: bool = False, first_name: str = None, last_name: str = None,
                 username: str = None, language_code: str = None, is_premium: bool = None,
                 added_to_attachment_menu: bool = None, can_join_groups: bool = None,
                 can_read_all_group_messages: bool = None, supports_inline_queries: bool = None,
                 can_connect_to_business: bool = None, has_main_web_app: bool = None):
        '''Создает объект User для представления информации о пользователе'''
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
    def from_dict(cls, data: dict) -> 'User':
        '''Создает объект User из словаря, возвращенного Telegram API'''
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
            has_main_web_app=data.get('has_main_web_app'))

    def __repr__(self) -> str:
        '''Возвращает строковое представление объекта User'''
        return (f"User(id={self.id}, is_bot={self.is_bot}, first_name={self.first_name}, "
                f"last_name={self.last_name}, username={self.username}, language_code={self.language_code}, "
                f"is_premium={self.is_premium}, added_to_attachment_menu={self.added_to_attachment_menu}, "
                f"can_join_groups={self.can_join_groups}, can_read_all_group_messages={self.can_read_all_group_messages}, "
                f"supports_inline_queries={self.supports_inline_queries}, can_connect_to_business={self.can_connect_to_business}, "
                f"has_main_web_app={self.has_main_web_app})")


class Chat:
    def __init__(self, chat_id: Union[int, str], chat_type: str, title: str = None, username: str = None,
                 first_name: str = None, last_name: str = None, is_forum: bool = None):
        '''Создает объект Chat для представления информации о чате'''
        self.id = chat_id
        self.type = chat_type
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.is_forum = is_forum

    @classmethod
    def from_dict(cls, data: dict) -> 'Chat':
        '''Создает объект Chat из словаря, возвращенного Telegram API'''
        return cls(
            chat_id=data['id'],
            chat_type=data['type'],
            title=data.get('title'),
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            is_forum=data.get('is_forum'))

    def __repr__(self) -> str:
        '''Возвращает строковое представление объекта Chat'''
        return (f"Chat(id={self.id}, type={self.type}, title={self.title}, username={self.username}, "
                f"first_name={self.first_name}, last_name={self.last_name}, is_forum={self.is_forum})")


class ChatMember:
    def __init__(self, user: 'User', status: str, **kwargs: dict):
        '''Создает объект ChatMember для представления информации о участнике чата'''
        self.user = user
        self.status = status
        # Поля ChatMemberOwner
        self.is_anonymous = kwargs.get('is_anonymous', None)
        self.custom_title = kwargs.get('custom_title', None)
        # Поля ChatMemberAdministrator
        self.can_be_edited = kwargs.get('can_be_edited', None)
        self.can_manage_chat = kwargs.get('can_manage_chat', None)
        self.can_delete_messages = kwargs.get('can_delete_messages', None)
        self.can_manage_video_chats = kwargs.get('can_manage_video_chats', None)
        self.can_restrict_members = kwargs.get('can_restrict_members', None)
        self.can_promote_members = kwargs.get('can_promote_members', None)
        self.can_change_info = kwargs.get('can_change_info', None)
        self.can_invite_users = kwargs.get('can_invite_users', None)
        self.can_pin_messages = kwargs.get('can_pin_messages', None)
        # Поля ChatMemberRestricted
        self.is_member = kwargs.get('is_member', None)
        self.until_date = kwargs.get('until_date', None)
        self.can_send_messages = kwargs.get('can_send_messages', None)
        self.can_send_media_messages = kwargs.get('can_send_media_messages', None)
        self.can_send_polls = kwargs.get('can_send_polls', None)
        self.can_send_other_messages = kwargs.get('can_send_other_messages', None)
        self.can_add_web_page_previews = kwargs.get('can_add_web_page_previews', None)
        # Поля ChatMemberBanned
        self.until_date = kwargs.get('until_date', None)

    @classmethod
    def from_dict(cls, data: dict) -> 'ChatMember':
        '''Создает объект ChatMember из словаря, возвращенного Telegram API'''
        user = User.from_dict(data['user'])
        status = data.get('status')
        if status == 'creator':
            return cls(user=user, status=status, is_anonymous=data.get('is_anonymous'), custom_title=data.get('custom_title'))
        elif status == 'administrator':
            return cls(
                user=user,
                status=status,
                can_be_edited=data.get('can_be_edited'),
                is_anonymous=data.get('is_anonymous'),
                can_manage_chat=data.get('can_manage_chat'),
                can_delete_messages=data.get('can_delete_messages'),
                can_manage_video_chats=data.get('can_manage_video_chats'),
                can_restrict_members=data.get('can_restrict_members'),
                can_promote_members=data.get('can_promote_members'),
                can_change_info=data.get('can_change_info'),
                can_invite_users=data.get('can_invite_users'),
                can_pin_messages=data.get('can_pin_messages'))
        elif status == 'restricted':
            return cls(
                user=user,
                status=status,
                is_member=data.get('is_member'),
                until_date=data.get('until_date'),
                can_send_messages=data.get('can_send_messages'),
                can_send_media_messages=data.get('can_send_media_messages'),
                can_send_polls=data.get('can_send_polls'),
                can_send_other_messages=data.get('can_send_other_messages'),
                can_add_web_page_previews=data.get('can_add_web_page_previews'))
        elif status == 'kicked':
            return cls(user=user, status=status, until_date=data.get('until_date'))
        else:
            return cls(user=user, status=status)

    def __repr__(self) -> str:
        '''Возвращает строковое представление объекта ChatMember'''
        return f"<ChatMember {self.user.first_name}, status: {self.status}>"


class ChatPermissions:
    def __init__(
        self,
        can_send_messages: bool = None,
        can_send_media_messages: bool = None,
        can_send_polls: bool = None,
        can_send_other_messages: bool = None,
        can_add_web_page_previews: bool = None,
        can_change_info: bool = None,
        can_invite_users: bool = None,
        can_pin_messages: bool = None,
        can_manage_topics: bool = None
    ):
        '''Создает объект ChatPermissions для управления правами участников чата'''
        self.can_send_messages = can_send_messages
        self.can_send_media_messages = can_send_media_messages
        self.can_send_polls = can_send_polls
        self.can_send_other_messages = can_send_other_messages
        self.can_add_web_page_previews = can_add_web_page_previews
        self.can_change_info = can_change_info
        self.can_invite_users = can_invite_users
        self.can_pin_messages = can_pin_messages
        self.can_manage_topics = can_manage_topics

    def to_dict(self):
        '''Преобразует объект ChatPermissions в словарь для отправки в Telegram API, игнорируя параметры с None значением'''
        return {k: v for k, v in {
            'can_send_messages': self.can_send_messages,
            'can_send_media_messages': self.can_send_media_messages,
            'can_send_polls': self.can_send_polls,
            'can_send_other_messages': self.can_send_other_messages,
            'can_add_web_page_previews': self.can_add_web_page_previews,
            'can_change_info': self.can_change_info,
            'can_invite_users': self.can_invite_users,
            'can_pin_messages': self.can_pin_messages,
            'can_manage_topics': self.can_manage_topics
        }.items() if v is not None}

    @classmethod
    def from_dict(cls, data: dict):
        '''Создает объект ChatPermissions из словаря, возвращенного Telegram API'''
        return cls(
            can_send_messages=data.get('can_send_messages'),
            can_send_media_messages=data.get('can_send_media_messages'),
            can_send_polls=data.get('can_send_polls'),
            can_send_other_messages=data.get('can_send_other_messages'),
            can_add_web_page_previews=data.get('can_add_web_page_previews'),
            can_change_info=data.get('can_change_info'),
            can_invite_users=data.get('can_invite_users'),
            can_pin_messages=data.get('can_pin_messages'),
            can_manage_topics=data.get('can_manage_topics')
        )

    def __repr__(self):
        '''Возвращает строковое представление объекта ChatPermissions'''
        return f'<ChatPermissions {self.to_dict()}>'


class PhotoSize:
    def __init__(self, file_id: str, file_unique_id: str, width: int, height: int, file_size: int = None):
        '''Создает объект PhotoSize, представляющий размер фотографии'''
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.file_size = file_size

    @classmethod
    def from_dict(cls, data: dict) -> 'PhotoSize':
        '''Создает объект PhotoSize из словаря, предоставленного Telegram API'''
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            width=data['width'],
            height=data['height'],
            file_size=data.get('file_size'))

    def __repr__(self) -> str:
        '''Возвращает строковое представление объекта PhotoSize'''
        return (f"PhotoSize(file_id={self.file_id}, file_unique_id={self.file_unique_id}, "
                f"width={self.width}, height={self.height}, file_size={self.file_size})")


class Photo:
    def __init__(self, file_id: str, file_unique_id: str, width: int, height: int):
        '''Создает объект Photo, представляющий фотографию'''
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height

    @classmethod
    def from_dict(cls, data: dict) -> 'Photo':
        '''Создает объект Photo из словаря, предоставленного Telegram API'''
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            width=data['width'],
            height=data['height'])


class Audio:
    def __init__(self, file_id: str, file_unique_id: str, duration: int, performer: str = None, title: str = None, thumbnail: dict = None):
        '''Создает объект Audio, представляющий аудиофайл'''
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.duration = duration
        self.performer = performer
        self.title = title
        self.thumbnail = PhotoSize.from_dict(thumbnail) if thumbnail else None

    @classmethod
    def from_dict(cls, data: dict) -> 'Audio':
        '''Создает объект Audio из словаря, предоставленного Telegram API'''
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            duration=data['duration'],
            performer=data.get('performer'),
            title=data.get('title'),
            thumbnail=data.get('thumbnail'))


class Voice:
    def __init__(self, file_id: str, file_unique_id: str, duration: int, mime_type: str = None, file_size: int = None, thumbnail: dict = None):
        '''Создает объект Voice, представляющий голосовое сообщение'''
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.duration = duration
        self.mime_type = mime_type
        self.file_size = file_size
        self.thumbnail = PhotoSize.from_dict(thumbnail) if thumbnail else None

    @classmethod
    def from_dict(cls, data: dict) -> 'Voice':
        '''Создает объект Voice из словаря, предоставленного Telegram API'''
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            duration=data['duration'],
            mime_type=data.get('mime_type'),
            file_size=data.get('file_size'),
            thumbnail=data.get('thumbnail'))


class Video:
    def __init__(self, file_id: str, file_unique_id: str, duration: int, width: int, height: int, thumbnail: dict = None):
        '''Создает объект Video, представляющий видеофайл'''
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.duration = duration
        self.width = width
        self.height = height
        self.thumbnail = PhotoSize.from_dict(thumbnail) if thumbnail else None

    @classmethod
    def from_dict(cls, data: dict) -> 'Video':
        '''Создает объект Video из словаря, предоставленного Telegram API'''
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            duration=data['duration'],
            width=data['width'],
            height=data['height'],
            thumbnail=data.get('thumbnail'))
    

class VideoNote:
    def __init__(self, file_id: str, file_unique_id: str, duration: int, length: int, thumbnail: dict = None, file_size: int = None):
        '''Создает объект VideoNote, представляющий видеозаметку'''
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.duration = duration
        self.length = length
        self.thumbnail = PhotoSize.from_dict(thumbnail) if thumbnail else None
        self.file_size = file_size

    @classmethod
    def from_dict(cls, data: dict) -> 'VideoNote':
        '''Создает объект VideoNote из словаря, предоставленного Telegram API'''
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            duration=data['duration'],
            length=data['length'],
            thumbnail=data.get('thumbnail'),
            file_size=data.get('file_size'))


class Animation:
    def __init__(self, file_id: str, file_unique_id: str, width: int, height: int, duration: int, 
                 thumbnail: dict = None, file_name: str = None, mime_type: str = None, file_size: int = None):
        '''Создает объект Animation, представляющий анимацию (GIF)'''
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
    def from_dict(cls, data: dict) -> 'Animation':
        '''Создает объект Animation из словаря, предоставленного Telegram API'''
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            width=data['width'],
            height=data['height'],
            duration=data['duration'],
            thumbnail=data.get('thumbnail'),
            file_name=data.get('file_name'),
            mime_type=data.get('mime_type'),
            file_size=data.get('file_size'))


class Dice:
    def __init__(self, emoji: str, value: int):
        '''Создает объект Dice, представляющий результат броска игральной кости'''
        self.emoji = emoji
        self.value = value

    @classmethod
    def from_dict(cls, data: dict) -> 'Dice':
        '''Создает объект Dice из словаря, предоставленного Telegram API'''
        return cls(
            emoji=data['emoji'],
            value=data['value'])


class Sticker:
    def __init__(self, file_id: str, file_unique_id: str, width: int, height: int, 
                 is_animated: bool, is_video: bool, thumbnail: dict = None):
        '''Создает объект Sticker, представляющий стикер'''
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.is_animated = is_animated
        self.is_video = is_video
        self.thumbnail = PhotoSize.from_dict(thumbnail) if thumbnail else None

    @classmethod
    def from_dict(cls, data: dict) -> 'Sticker':
        '''Создает объект Sticker из словаря, предоставленного Telegram API'''
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            width=data['width'],
            height=data['height'],
            is_animated=data.get('is_animated', False),
            is_video=data.get('is_video', False),
            thumbnail=data.get('thumbnail'))


class Document:
    def __init__(self, file_id: str, file_unique_id: str, file_name: str = None, 
                 mime_type: str = None, file_size: int = None, thumbnail: dict = None):
        '''Создает объект Document, представляющий документ'''
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
        self.thumbnail = PhotoSize.from_dict(thumbnail) if thumbnail else None

    @classmethod
    def from_dict(cls, data: dict) -> 'Document':
        '''Создает объект Document из словаря, предоставленного Telegram API'''
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            file_name=data.get('file_name'),
            mime_type=data.get('mime_type'),
            file_size=data.get('file_size'),
            thumbnail=data.get('thumbnail'))
    

class File:
    def __init__(self, file_id: str, file_unique_id: str, file_size: int, file_path: str = None):
        '''Создает объект File, представляющий общий файл'''
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_size = file_size
        self.file_path = file_path

    @classmethod
    def from_dict(cls, data: dict) -> 'File':
        '''Создает объект File из словаря, предоставленного Telegram API'''
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            file_size=data['file_size'],
            file_path=data.get('file_path'))


class WebhookInfo:
    def __init__(self, url: str = None, has_custom_certificate: bool = None, 
                 pending_update_count: int = None, last_error_date: int = None, 
                 last_error_message: str = None, max_connections: int = None, 
                 allowed_updates: list = None):
        '''Создает объект WebhookInfo, представляющий информацию о вебхуке'''
        self.url = url
        self.has_custom_certificate = has_custom_certificate
        self.pending_update_count = pending_update_count
        self.last_error_date = last_error_date
        self.last_error_message = last_error_message
        self.max_connections = max_connections
        self.allowed_updates = allowed_updates

    @classmethod
    def from_dict(cls, data: dict) -> 'WebhookInfo':
        '''Создает объект WebhookInfo из словаря, предоставленного Telegram API'''
        return cls(
            url=data.get('url'),
            has_custom_certificate=data.get('has_custom_certificate'),
            pending_update_count=data.get('pending_update_count'),
            last_error_date=data.get('last_error_date'),
            last_error_message=data.get('last_error_message'),
            max_connections=data.get('max_connections'),
            allowed_updates=data.get('allowed_updates'))


class InputFile:
    def __init__(self, file_path: str):
        '''Создает объект InputFile, представляющий файл для отправки через Telegram Bot API'''
        self.file_path = file_path

    def __str__(self) -> str:
        return self.file_path


class InputMedia:
    def __init__(self, media: str, caption: str = None, mode: str = None, caption_entities: list = None):
        '''Базовый класс для всех типов медиа контента, отправляемого через Telegram Bot API'''
        self.media = media
        self.caption = caption
        self.mode = mode
        self.caption_entities = caption_entities

    def to_dict(self) -> dict:
        '''Создает словарь с данными для отправки медиа'''
        data = {'media': self.media}
        if self.caption:
            data['caption'] = self.caption
        if self.mode:
            data['parse_mode'] = self.mode
        if self.caption_entities:
            data['caption_entities'] = [entity.to_dict() for entity in self.caption_entities]
        return data

class InputMediaPhoto(InputMedia):
    def __init__(self, media: str, caption: str = None, mode: str = "Markdown", 
                 caption_entities: list = None, show_caption_above_media: bool = None, has_spoiler: bool = None):
        '''Создает объект InputMediaPhoto, для отправки фото через Telegram Bot API'''
        super().__init__(media, caption, mode, caption_entities)
        self.type = 'photo'
        self.show_caption_above_media = show_caption_above_media
        self.has_spoiler = has_spoiler

    def to_dict(self) -> dict:
        '''Создает словарь с данными для отправки фото'''
        data = super().to_dict()
        data['type'] = self.type
        if self.show_caption_above_media is not None:
            data['show_caption_above_media'] = self.show_caption_above_media
        if self.has_spoiler is not None:
            data['has_spoiler'] = self.has_spoiler
        return data

class InputMediaVideo(InputMedia):
    def __init__(self, media: str, caption: str = None, mode: str = "Markdown", 
                 caption_entities: list = None, show_caption_above_media: bool = None, 
                 width: int = None, height: int = None, duration: int = None, 
                 supports_streaming: bool = False, has_spoiler: bool = None):
        '''Создает объект InputMediaVideo, для отправки видео через Telegram Bot API'''
        super().__init__(media, caption, mode, caption_entities)
        self.type = 'video'
        self.show_caption_above_media = show_caption_above_media
        self.width = width
        self.height = height
        self.duration = duration
        self.supports_streaming = supports_streaming
        self.has_spoiler = has_spoiler

    def to_dict(self) -> dict:
        '''Создает словарь с данными для отправки видео'''
        data = super().to_dict()
        data.update({'type': self.type, 'supports_streaming': self.supports_streaming})
        if self.width:
            data['width'] = self.width
        if self.height:
            data['height'] = self.height
        if self.duration:
            data['duration'] = self.duration
        if self.show_caption_above_media is not None:
            data['show_caption_above_media'] = self.show_caption_above_media
        if self.has_spoiler is not None:
            data['has_spoiler'] = self.has_spoiler
        return data

class InputMediaAnimation(InputMedia):
    def __init__(self, media: str, caption: str = None, mode: str = "Markdown", 
                 caption_entities: list = None, show_caption_above_media: bool = None, 
                 width: int = None, height: int = None, duration: int = None, has_spoiler: bool = None):
        '''
        Создает объект InputMediaAnimation для отправки анимации через Telegram Bot API'''
        super().__init__(media, caption, mode, caption_entities)
        self.type = 'animation'
        self.width = width
        self.height = height
        self.duration = duration
        self.show_caption_above_media = show_caption_above_media
        self.has_spoiler = has_spoiler

    def to_dict(self) -> dict:
        '''Создает словарь с данными для отправки анимации'''
        data = super().to_dict()
        data['type'] = self.type
        if self.width:
            data['width'] = self.width
        if self.height:
            data['height'] = self.height
        if self.duration:
            data['duration'] = self.duration
        if self.show_caption_above_media is not None:
            data['show_caption_above_media'] = self.show_caption_above_media
        if self.has_spoiler is not None:
            data['has_spoiler'] = self.has_spoiler
        return data

class InputMediaAudio(InputMedia):
    def __init__(self, media: str, caption: str = None, mode: str = "Markdown", caption_entities: list = None,
                 duration: int = None, performer: str = None, title: str = None):
        '''Создает объект InputMediaAudio для отправки аудиофайлов через Telegram Bot API'''
        super().__init__(media, caption, mode, caption_entities)
        self.type = 'audio'
        self.duration = duration
        self.performer = performer
        self.title = title

    def to_dict(self) -> dict:
        '''Создает словарь с данными для отправки аудио'''
        data = super().to_dict()
        data['type'] = self.type
        if self.duration:
            data['duration'] = self.duration
        if self.performer:
            data['performer'] = self.performer
        if self.title:
            data['title'] = self.title
        return data

class InputMediaDocument(InputMedia):
    def __init__(self, media: str, caption: str = None, mode: str = "Markdown", 
                 caption_entities: list = None, disable_content_type_detection: bool = False):
        '''Создает объект InputMediaDocument для отправки документов через Telegram Bot API'''
        super().__init__(media, caption, mode, caption_entities)
        self.type = 'document'
        self.disable_content_type_detection = disable_content_type_detection

    def to_dict(self) -> dict:
        '''Создает словарь с данными для отправки документа'''
        data = super().to_dict()
        data['type'] = self.type
        if self.disable_content_type_detection:
            data['disable_content_type_detection'] = self.disable_content_type_detection
        return data


class CallbackQuery:
    def __init__(self, callback_query_data: dict):
        '''Создает объект CallbackQuery для обработки callback-запросов в Telegram Bot API'''
        self.id = callback_query_data['id']
        self.from_user = User.from_dict(callback_query_data['from'])
        self.data = callback_query_data.get('data')
        self.message = Message.from_dict(callback_query_data['message']) if callback_query_data.get('message') else None
        self.inline_message_id = callback_query_data.get('inline_message_id')
        self.chat_instance = callback_query_data.get('chat_instance')
        self.game_short_name = callback_query_data.get('game_short_name')
    

class Markup:
    @staticmethod
    def create_reply_keyboard(buttons: list[dict], row_width: int = 2, is_persistent: bool = False, resize_keyboard: bool = True, one_time_keyboard: bool = False) -> dict:
        '''Создание **reply** клавиатуры'''
        if not buttons:
            raise ValueError("buttons не может быть None")
        keyboard = []
        for i in range(0, len(buttons), row_width):
            keyboard.append(buttons[i:i + row_width])
        return {'keyboard': keyboard, 'is_persistent': is_persistent, 'resize_keyboard': resize_keyboard, 'one_time_keyboard': one_time_keyboard}

    @staticmethod
    def remove_reply_keyboard(status: bool = True) -> dict:
        '''Удаляет/Показывает **reply** клавиатуры'''
        return {'remove_keyboard': status}

    @staticmethod
    def create_inline_keyboard(buttons: list[dict], row_width: int = 2) -> dict:
        '''Создаёт **inline** клавиатуру'''
        if not buttons:
            raise ValueError("buttons не может быть None")
        keyboard = []
        for i in range(0, len(buttons), row_width):
            keyboard.append(buttons[i:i + row_width])
        return {'inline_keyboard': keyboard}


class MessageEntity:
    def __init__(self, type: str, offset: int, length: int, url: str = None,
                 user: dict = None, language: str = None):
        '''Создает объект MessageEntity для описания форматирования текста'''
        self.type = type
        self.offset = offset
        self.length = length
        self.url = url
        self.user = user
        self.language = language

    def to_dict(self) -> dict:
        '''Возвращает словарь с данными MessageEntity'''
        data = {
            'type': self.type,
            'offset': self.offset,
            'length': self.length,
            'url': self.url,
            'user': self.user,
            'language': self.language}
        return {k: v for k, v in data.items() if v is not None}


class Message:
    def __init__(self, message_id: int, chat: 'Chat', from_user: 'User', text: str = None, 
                 date: int = None, reply_to_message: 'Message' = None, content_type: str = None, 
                 photo: list = None, audio: 'Audio' = None, video: 'Video' = None, 
                 video_note: 'VideoNote' = None, voice: 'Voice' = None, animation: 'Animation' = None, 
                 dice: 'Dice' = None, sticker: 'Sticker' = None, document: 'Document' = None, 
                 new_chat_members: list = None, new_chat_member: 'User' = None, 
                 left_chat_member: 'User' = None):
        '''Инициализирует объект сообщения (Message), представляющий отправленное сообщение в чате'''
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
    def from_dict(cls, data: dict) -> 'Message':
        '''Создает объект Message из словаря, предоставленного Telegram API'''
        chat = Chat.from_dict(data['chat'])
        from_user = User.from_dict(data['from']) if 'from' in data else None
        reply_to_message = Message.from_dict(data['reply_to_message']) if 'reply_to_message' in data else None
        content_type = None
        text = None
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
        if 'text' in data:
            content_type = 'text'
            text = data['text']
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
            left_chat_member=left_chat_member)


#Основа
class Bot:
    def __init__(self, token):
        '''Создает экземпляр Bot'''
        self.token = token
        self.handlers = {'message': [], 'command': [], 'callback_query': []}
        self.running = False
        self.update_offset = 0
        self.next_steps = {}

    def _make_request(self, method, params=None, files=None, json=None):
        '''Отправляет запрос в Telegram API с обработкой всех ошибок и повторными попытками'''
        url = f'https://api.telegram.org/bot{self.token}/{method}'
        max_retries = 5
        retry_after = 5
        for attempt in range(max_retries):
            try:
                response = requests.post(url, params=params, files=files, json=json)
                if response.status_code == 200:
                    return response.json()
                if response.status_code == 429:
                    retry_after = response.json().get('parameters', {}).get('retry_after', retry_after)
                    print(f"Ошибка 429 в методе {method}: Превышен лимит запросов. Повтор через {retry_after} секунд")
                    time.sleep(retry_after)
                elif response.status_code == 502:
                    print(f"Ошибка 502 в методе {method}: Bad Gateway. Попытка повторить запрос через несколько секунд...")
                    time.sleep(random.uniform(2, 5))
                elif response.status_code == 503:
                    print(f"Ошибка 503 в методе {method}: Сервис недоступен. Повтор через несколько секунд...")
                    time.sleep(random.uniform(5, 10))
                elif response.status_code == 400:
                    print(f"Ошибка 400 в методе {method}: Неверный запрос. {response.text}")
                    return None
                elif response.status_code == 404:
                    print(f"Ошибка 404 в методе {method}: Страница не найдена. {response.text}")
                    return None
                else:
                    print(f"Неизвестная ошибка в методе {method}: {response.status_code} - {response.text}")
                    return None
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при отправке запроса: {e}")
                return None
            except Exception as e:
                print(f"Необработанная ошибка: {e}")
                return None
            time.sleep(2 ** attempt + random.uniform(0, 1))
        print(f"Не удалось выполнить запрос {method} после {max_retries} попыток")
        return None

    def reply_message(self, chat_id: Union[int, str], text: str, mode: str = "Markdown", disable_web_page_preview: bool = None, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''Отправляет сообщение'''
        method = 'sendMessage'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not text:
            raise ValueError("text не должен быть None")
        params = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': mode,
            'disable_web_page_preview': disable_web_page_preview,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            return None

    def reply_photo(self, chat_id: Union[int, str], photo: Union[str, bytes], caption: str = None, mode: str = "Markdown", disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''Отправляет фото'''
        method = 'sendPhoto'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not photo:
            raise ValueError("photo не должен быть None")
        params = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': mode,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        if isinstance(photo, str):
            params['photo'] = photo
            files = None
        else:
            files = {'photo': photo}
        response = self._make_request(method, params, files)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            return None

    def reply_audio(self, chat_id: Union[int, str], audio: Union[str, bytes], caption: str = None, mode: str = "Markdown", duration: int = None, performer: str = None, title: str = None, thumb: Union[str, bytes] = None, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''Отправляет аудио'''
        method = 'sendAudio'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not audio:
            raise ValueError("audio не должен быть None")
        params = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': mode,
            'duration': duration,
            'performer': performer,
            'title': title,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
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
            return None

    def reply_document(self, chat_id: Union[int, str], document: Union[str, bytes], caption: str = None, mode: str = "Markdown", disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''Отправляет документ'''
        method = 'sendDocument'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not document:
            raise ValueError("document не должен быть None")
        params = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': mode,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        if isinstance(document, str):
            params['document'] = document
            files = None
        else:
            files = {'document': document}
        response = self._make_request(method, params, files)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            return None

    def reply_video(self, chat_id: Union[int, str], video: Union[str, bytes], duration: int = None, width: int = None, height: int = None, caption: str = None, mode: str = "Markdown", supports_streaming: bool = None, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''Отправляет видео'''
        method = 'sendVideo'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not video:
            raise ValueError("video не должен быть None")
        params = {
            'chat_id': chat_id,
            'duration': duration,
            'width': width,
            'height': height,
            'caption': caption,
            'parse_mode': mode,
            'supports_streaming': supports_streaming,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        if isinstance(video, str):
            params['video'] = video
            files = None
        else:
            files = {'video': video}
        response = self._make_request(method, params, files)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            return None

    def reply_video_note(self, chat_id: Union[int, str], video_note: Union[str, bytes], duration: int = None, length: int = None, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''Отправляет видео кружочек'''
        method = 'sendVideoNote'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not video_note:
            raise ValueError("video_note не должен быть None")
        params = {
            'chat_id': chat_id,
            'duration': duration,
            'length': length,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        if isinstance(video_note, str):
            params['video_note'] = video_note
            files = None
        else:
            files = {'video_note': video_note}
        response = self._make_request(method, params, files)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            return None

    def reply_animation(self, chat_id: Union[int, str], animation: Union[str, bytes], duration: int = None, width: int = None, height: int = None, caption: str = None, mode: str = "Markdown", disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''Отправляет анимацию'''
        method = 'sendAnimation'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not animation:
            raise ValueError("animation не должен быть None")
        params = {
            'chat_id': chat_id,
            'duration': duration,
            'width': width,
            'height': height,
            'caption': caption,
            'parse_mode': mode,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        if isinstance(animation, str):
            params['animation'] = animation
            files = None
        else:
            files = {'animation': animation}
        response = self._make_request(method, params, files)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            return None

    def reply_voice(self, chat_id: Union[int, str], voice: Union[str, bytes], caption: str = None, mode: str = "Markdown", duration: int = None, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''Отправляет голосовое сообщение'''
        method = 'sendVoice'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not voice:
            raise ValueError("voice не должен быть None")
        params = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': mode,
            'duration': duration,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        if isinstance(voice, str):
            params['voice'] = voice
            files = None
        else:
            files = {'voice': voice}
        response = self._make_request(method, params, files)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            return None

    def reply_location(self, chat_id: Union[int, str], latitude: float, longitude: float, live_period: int = None, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''Отправляет локацию в chat_id'''
        method = 'sendLocation'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not latitude:
            raise ValueError("latitude не должен быть None")
        elif not longitude:
            raise ValueError("longitude не может быть None")
        params = {
            'chat_id': chat_id,
            'latitude': latitude,
            'longitude': longitude,
            'live_period': live_period,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            return None

    def reply_chat_action(self, chat_id: Union[int, str], action: str) -> bool:
        '''Отправляет активность'''
        method = 'sendChatAction'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not action:
            raise ValueError("action не должен быть None")
        params = {'chat_id': chat_id, 'action': action}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False
    
    def reply_venue(self, chat_id: Union[int, str], latitude: float, longitude: float, title: str, address: str, foursquare_id: str = None, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''Отправляет место (venue) в chat_id'''
        method = 'sendVenue'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not latitude:
            raise ValueError("latitude не должен быть None")
        elif not longitude:
            raise ValueError("longitude не может быть None")
        params = {
            'chat_id': chat_id,
            'latitude': latitude,
            'longitude': longitude,
            'title': title,
            'address': address,
            'foursquare_id': foursquare_id,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            return None
    
    def reply_contact(self, chat_id: Union[int, str], phone_number: str, first_name: str, last_name: str = None, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''Отправляет контакт в chat_id'''
        method = 'sendContact'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not phone_number:
            raise ValueError("phone_number не должен быть None")
        elif not first_name:
            raise ValueError("first_name не может быть None")
        params = {
            'chat_id': chat_id,
            'phone_number': phone_number,
            'first_name': first_name,
            'last_name': last_name,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            return None
    
    def reply_sticker(self, chat_id: Union[int, str], sticker: Union[str, bytes], disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''Отправляет стикер в chat_id'''
        method = 'sendSticker'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not sticker:
            raise ValueError("sticker не должен быть None")
        params = {
            'chat_id': chat_id,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        if isinstance(sticker, str):
            params['sticker'] = sticker
            files = None
        else:
            files = {'sticker': sticker}
        response = self._make_request(method, params, files)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        else:
            return None
        
    def reply_dice(self, chat_id: Union[int, str], emoji: str, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''Отправляет анимированные эмодзи в chat_id'''
        method = 'sendDice'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not emoji:
            raise ValueError("emoji не должен быть None")
        params = {
            'chat_id': chat_id,
            'emoji': emoji,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def reply_message_reaction(self, chat_id: Union[int, str], message_id: int, reaction: str = '👍', is_big: bool = False) -> bool:
        '''Отправить реакцию'''
        method = 'setMessageReaction'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not message_id:
            raise ValueError("message_id не должен быть None")
        elif not reaction:
            raise ValueError("reaction не должен быть None")
        params = {
            'chat_id': chat_id,
            'message_id': message_id,
            'reaction': [{'type': 'emoji', 'emoji': reaction}],
            'is_big': is_big}
        response = self._make_request(method, json=params)
        if response and 'result' in response:
            return True
        else:
            return False


    def reply_poll(self, chat_id: Union[int, str], question: str, options: list, is_anonymous: bool = False, type: str = 'regular', allows_multiple_answers: bool = False, correct_option_id: int = None, explanation: str = None, mode: str = "Markdown", open_period: int = None, close_date: int = None, is_closed: bool = False, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> bool:
        '''Отправляет опрос в chat_id'''
        method = 'sendPoll'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not question:
            raise ValueError("question не должен быть None")
        elif not options:
            raise ValueError("options не должен быть None")
        if not isinstance(options, list):
            raise ValueError("options должны быть списком")
        params = {
            'chat_id': chat_id,
            'question': question,
            'options': json.dumps(options),
            'is_anonymous': is_anonymous,
            'type': type,
            'allows_multiple_answers': allows_multiple_answers,
            'correct_option_id': correct_option_id,
            'explanation': explanation,
            'explanation_parse_mode': mode,
            'open_period': open_period,
            'close_date': close_date,
            'is_closed': is_closed,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False
    
    def stop_poll(self, chat_id: Union[int, str], message_id: int, reply_markup: Union[dict, Markup] = None) -> bool:
        '''Завершает активный опрос в чате'''
        method = 'stopPoll'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not message_id:
            raise ValueError("message_id не должен быть None")
        params = {'chat_id': chat_id, 'message_id': message_id, 'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False
        
    def pin_message(self, chat_id: Union[int, str], message_id: int) -> bool:
        '''Закрепляет сообщение в чате'''
        method = 'pinChatMessage'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not message_id:
            raise ValueError("message_id не должен быть None")
        params = {'chat_id': chat_id, 'message_id': message_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def unpin_message(self, chat_id: Union[int, str], message_id: int) -> bool:
        '''Открепляет сообщение в чате'''
        method = 'unpinChatMessage'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not message_id:
            raise ValueError("message_id не должен быть None")
        params = {'chat_id': chat_id, 'message_id': message_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def forward_message(self, chat_id: Union[int, str], from_chat_id: Union[int, str], message_id: int, disable_notification: bool = None) -> bool:
        '''Пересылает сообщение'''
        method = 'forwardMessage'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not from_chat_id:
            raise ValueError("from_chat_id не должен быть None")
        elif not message_id:
            raise ValueError("message_id не должен быть None")
        params = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'message_id': message_id,
            'disable_notification': disable_notification}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False
    
    def forward_messages(self, chat_id: Union[int, str], from_chat_id: Union[int, str], message_ids: Union[int, list], disable_notification: bool = None) -> bool:
        '''Пересылает несколько сообщений'''
        method = 'forwardMessages'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not from_chat_id:
            raise ValueError("from_chat_id не должен быть None")
        elif not message_ids:
            raise ValueError("message_ids не должен быть None")
        params = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'message_ids': message_ids,
            'disable_notification': disable_notification}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def copy_message(self, chat_id: Union[int, str], from_chat_id: Union[int, str], message_id: int, caption: str = None, disable_notification: bool = None, mode: str = "Markdown", reply_markup: Union[dict, Markup] = None) -> bool:
        '''Копирует сообщение'''
        method = 'copyMessage'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not from_chat_id:
            raise ValueError("from_chat_id не должен быть None")
        elif not message_id:
            raise ValueError("message_id не должен быть None")
        params = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'message_id': message_id,
            'caption': caption,
            'parse_mode': mode,
            'disable_notification': disable_notification,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False
    
    def copy_messages(self, chat_id: Union[int, str], from_chat_id: Union[int, str], message_ids: Union[int, list], disable_notification: bool = None) -> bool:
        '''Копирует несколько сообщений'''
        method = 'copyMessages'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not from_chat_id:
            raise ValueError("from_chat_id не должен быть None")
        elif not message_ids:
            raise ValueError("message_ids не должен быть None")
        params = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'message_ids': message_ids,
            'disable_notification': disable_notification}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def delete_message(self, chat_id: Union[int, str], message_id: int) -> bool:
        '''Удаляет сообщение'''
        method = 'deleteMessage'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not message_id:
            raise ValueError("message_id не должен быть None")
        params = {'chat_id': chat_id, 'message_id': message_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def delete_messages(self, chat_id: Union[int, str], message_ids: Union[int, list]) -> bool:
        '''Удаляет все сообщения'''
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not message_ids:
            raise ValueError("message_ids не должен быть None")
        for message_id in message_ids:
            self.delete_message(chat_id, message_id)

    def get_user_profile_photos(self, user_id: int, offset: int = None, limit: int = None, photo_index: int = None) -> Optional[str]:
        '''Получает список фотографий профиля пользователя
        
        :param user_id: Идентификатор пользователя
        :param offset: Смещение для получения фотографий
        :param limit: Максимальное количество фотографий для получения
        :param photo_index: Индекс фотографии для возврата (последнее фото из доступных)
        :return: file_id запрашиваемого фото или file_id последнего загруженного фото
        '''
        method_url = 'getUserProfilePhotos'
        if user_id is None:
            raise ValueError("user_id не должен быть None")
        params = {'user_id': user_id, 'offset': offset, 'limit': limit}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method_url, params=params)
        if response and 'result' in response:
            photos = response['result']['photos']
            if photos:
                if photo_index is not None:
                    if 0 <= photo_index < len(photos):
                        selected_photo = photos[photo_index][-1]
                        return selected_photo['file_id']
                    else:
                        raise IndexError("photo_index выходит за пределы списка фотографий")
                else:
                    last_photo = photos[-1][-1]
                    return last_photo['file_id']
            else:
                return None
        else:
            return None
    
    def get_me(self) -> Optional['User']:
        '''Возвращает объект бота'''
        method = 'getMe'
        response = self._make_request(method)
        if 'result' in response:
            return User.from_dict(response['result'])
        else:
            return None

    def get_file(self, file_id: str) -> Optional['File']:
        '''Получает информацию о файле на серверах Telegram'''
        method = 'getFile'
        if not file_id:
            raise ValueError("file_id не может быть None")
        params = {'file_id': file_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return File.from_dict(response['result'])
        else:
            return None

    def download_file(self, file: str, save_path: str, chunk_size: int = 1024, timeout: int = 60, headers=None, stream: bool = True) -> bool:
        '''Скачивает файл с серверов Telegram и сохраняет на диск'''
        if not isinstance(file, File):
            raise ValueError("file должен быть объектом класса TelegramFile")
        if not file.file_path:
            raise ValueError("file_path не должен быть None")
        elif not save_path:
            raise ValueError("save_path не должен быть None")
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
                    print(f"Ошибка при скачивании файла: {response.json()}")
                    return False
        except requests.exceptions.RequestException as e:
            print(f"Произошла ошибка при скачивании файла: {e}")

#Редакт чего-то
    def edit_message_text(self, chat_id: Union[int, str], message_id: int, text: str, inline_message_id: str = None, mode="Markdown", reply_markup: Union[dict, Markup] = None) -> bool:
        '''Редактирует текст сообщения'''
        method = 'editMessageText'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not message_id:
            raise ValueError("message_id не должен быть None")
        elif not text:
            raise ValueError("text не должен быть None")
        params = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text,
            'parse_mode': mode,
            'inline_message_id': inline_message_id,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def edit_message_caption(self, chat_id: Union[int, str], message_id: int, caption: str, inline_message_id: str = None, mode: str = "Markdown", show_caption_above_media: bool = False, reply_markup: Union[dict, Markup] = None) -> bool:
        '''Редактирует описание медиа'''
        method = 'editMessageCaption'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not message_id:
            raise ValueError("message_id не должен быть None")
        elif not caption:
            raise ValueError("caption не должен быть None")
        params = {
            'chat_id': chat_id,
            'message_id': message_id,
            'caption': caption,
            'parse_mode': mode,
            'inline_message_id': inline_message_id,
            'show_caption_above_media': show_caption_above_media,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def edit_message_media(self, chat_id: Union[int, str], message_id: int, media: Union[str, bytes, InputMediaPhoto, InputMediaAnimation, InputMediaVideo, InputMediaAudio, InputMediaDocument], caption: str = None, mode: str = "Markdown", inline_message_id: str = None, reply_markup: Union[dict, Markup] = None) -> bool:
        '''Редактирует медиа сообщение'''
        method = 'editMessageMedia'
        files = None
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not message_id:
            raise ValueError("message_id не должен быть None")
        elif not media:
            raise ValueError("media не должен быть None")
        if isinstance(media, (InputMediaPhoto, InputMediaAnimation, InputMediaVideo, InputMediaAudio, InputMediaDocument)):
            media_payload = media.to_dict()
        elif isinstance(media, str):
            media_payload = {'type': 'photo', 'media': media}
        elif isinstance(media, bytes):
            media_payload = {'type': 'photo', 'media': 'attach://media'}
            files = {'media': media}
        else:
            raise ValueError('media должно быть экземпляром str, bytes, или одного из классов InputMedia.')
        params = {
            'chat_id': chat_id,
            'message_id': message_id,
            'media': media_payload,
            'caption': caption,
            'parse_mode': mode,
            'inline_message_id': inline_message_id,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, json=params, files=files)
        if response and 'result' in response:
            return True
        else:
            return False

    def edit_message_reply_markup(self, chat_id: Union[int, str], message_id: int, reply_markup: Union[dict, Markup], inline_message_id: str = None) -> bool:
        '''Редактирует клавиатуру сообщения'''
        method = 'editMessageReplyMarkup'
        if not chat_id:
            raise ValueError("chat_id не должен быть None")
        elif not message_id:
            raise ValueError("message_id не должен быть None")
        elif not reply_markup:
            raise ValueError("reply_markup не должен быть None")
        params = {
            'chat_id': chat_id,
            'message_id': message_id,
            'inline_message_id': inline_message_id,
            'reply_markup': json.dumps(reply_markup)}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

#Вэбхук    
    def set_webhook(self, url: str, certificate: str = None, max_connections: int = None, allowed_updates: list | str = None) -> Optional['WebhookInfo']:
        '''Устанавливает вебхук'''
        method = 'setWebhook'
        if not url:
            raise ValueError("url не может быть None")
        params = {
            'url': url,
            'max_connections': max_connections,
            'allowed_updates': json.dumps(allowed_updates) if allowed_updates else None}
        params = {k: v for k, v in params.items() if v is not None}
        files = {'certificate': certificate} if certificate else None
        response = self._make_request(method, params, files)
        if response and 'result' in response:
            return WebhookInfo.from_dict(response['result'])
        else:
            return None

    def get_webhook_info(self, timeout: int = 30, drop_pending_updates: bool = None) -> Optional['WebhookInfo']:
        '''Получает информацию о текущем webhook.'''
        method = 'getWebhookInfo'
        params = {'timeout': timeout,
                   'drop_pending_updates': drop_pending_updates}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params=params)
        if response and 'result' in response:
            return WebhookInfo.from_dict(response['result'])
        else:
            return None
    
    def delete_webhook(self, drop_pending_updates: bool = False) -> bool:
        '''Удаляет вебхук'''
        method = 'deleteWebhook'
        params = {'drop_pending_updates': drop_pending_updates}
        response = self._make_request(method, params=params)
        if response and 'result' in response:
            return True
        else:
            return False

#Получение апдейтов
    def get_updates(self, timeout: int = 30, allowed_updates: Union[list, str] = None, long_polling_timeout: int = 30) -> list:
        '''Запрос обновлений с учетом дополнительных параметров'''
        method = 'getUpdates'
        params = {'timeout': timeout, 'allowed_updates': allowed_updates, 'offset': self.update_offset, 'long_polling_timeout': long_polling_timeout}
        params = {k: v for k, v in params.items() if v is not None}
        updates = self._make_request(method, params)
        if updates and 'result' in updates:
            return updates['result']
        return []

    def process_updates(self, updates: list):
        '''Обрабатывает полученные обновления'''
        if not updates:
            raise ValueError("updates не должен быть None")
        for update in updates:
            if 'message' in update:
                self._handle_message(update['message'])
                self.update_offset = update['update_id'] + 1
            elif 'callback_query' in update:
                self._handle_callback_query(update['callback_query'])
                self.update_offset = update['update_id'] + 1
    
    def polling(self, interval: int = 1):
        '''Передает обновления в течение длительного промежутка времени'''
        self.running = True
        while self.running:
            updates = self.get_updates()
            if updates:
                self.process_updates(updates)
            time.sleep(interval)

    def always_polling(self, interval: int = 1, timeout: int = 30, long_polling_timeout: int = 30, allowed_updates: Union[list, str] = None, restart_on_error: bool = True):
        '''Продолжает работу бесконечно, игнорируя ошибки и поддерживает параметры управления'''
        self.running = True
        while self.running:
            try:
                updates = self.get_updates(timeout=timeout, allowed_updates=allowed_updates, long_polling_timeout=long_polling_timeout)
                if updates:
                    self.process_updates(updates)
            except Exception as e:
                if not restart_on_error:
                    self.running = False
            time.sleep(interval)

    def stop_polling(self):
        '''Останавливает получение обновлений'''
        self.running = False

#Чат инфа
    def get_chat(self, chat_id: Union[int, str]) -> Optional['Chat']:
        '''Получает информацию о чате'''
        method = 'getChat'
        if not chat_id:
            raise ValueError("chat_id не может быть None")
        params = {'chat_id': chat_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Chat.from_dict(response['result'])
        else:
            return None

    def get_chat_administrators(self, chat_id: Union[int, str]) -> Union['ChatMember', list]:
        '''Получает список администраторов чата'''
        method = 'getChatAdministrators'
        if not chat_id:
            raise ValueError("chat_id не может быть None")
        params = {'chat_id': chat_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return [ChatMember.from_dict(admin) for admin in response['result']]
        else:
            return []

    def get_chat_members_count(self, chat_id: Union[int, str]) -> int:
        '''Получает количество участников чата'''
        method = 'getChatMemberCount'
        if not chat_id:
            raise ValueError("chat_id не может быть None")
        params = {'chat_id': chat_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return response['result']
        else:
            return 0

    def get_chat_member(self, chat_id: Union[int, str], user_id: int) -> Optional['ChatMember']:
        '''Получает информацию о пользователе чата и его статус'''
        method = 'getChatMember'
        if not chat_id:
            raise ValueError("chat_id не может быть None")
        elif not user_id:
            raise ValueError("user_id не может быть None")
        params = {'chat_id': chat_id, 'user_id': user_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return ChatMember.from_dict(response['result'])
        else:
            return None

    def set_chat_photo(self, chat_id: Union[int, str], photo: Union[str, bytes, InputFile]) -> bool:
        '''Устанавливает фото для чата'''
        method = 'setChatPhoto'
        if not chat_id:
            raise ValueError("chat_id не может быть None")
        elif not photo:
            raise ValueError("photo не может быть None")
        params = {'chat_id': chat_id}
        files = None
        if isinstance(photo, InputFile):
            with open(photo.file_path, 'rb') as f:
                files = {'photo': f}
        elif isinstance(photo, str):
            if photo.startswith('http'):
                params['photo'] = photo
            else:
                with open(photo, 'rb') as f:
                    files = {'photo': f}
        else:
            raise ValueError("Неверный формат фото. Ожидается InputFile, путь к файлу, file_id или URL.")
        response = self._make_request(method, params, files)
        if response and 'result' in response:
            return True
        else:
            return False

    def delete_chat_photo(self, chat_id: Union[int, str]) -> bool:
        '''Удаляет фотографию чата'''
        method = 'deleteChatPhoto'
        if not chat_id:
            raise ValueError("chat_id не может быть None")
        params = {'chat_id': chat_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def set_chat_title(self, chat_id: Union[int, str], title: str) -> bool:
        '''Устанавливает название чата'''
        method = 'setChatTitle'
        if not chat_id:
            raise ValueError("chat_id не может быть None")
        elif not title:
            raise ValueError("title не может быть None")
        elif len(title) < 1 or len(title) > 128:
            raise ValueError("Название чата должно быть от 1 до 128 символов")
        params = {'chat_id': chat_id, 'title': title}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def set_chat_description(self, chat_id: Union[int, str], description: str) -> bool:
        '''Устанавливает описание для чата'''
        method = 'setChatDescription'
        if not chat_id:
            raise ValueError("chat_id не может быть None")
        elif not description:
            raise ValueError("description не может быть None")
        elif len(description) < 0 or len(description) > 255:
            raise ValueError("Описание чата должно быть от 0 до 255 символов")
        params = {'chat_id': chat_id, 'description': description}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def leave_chat(self, chat_id: Union[int, str]) -> bool:
        '''Покидает чат'''
        method = 'leaveChat'
        if not chat_id:
            raise ValueError("chat_id не может быть None")
        params = {'chat_id': chat_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False
    
# Административные команды
    def kick_chat_member(self, chat_id: Union[int, str], user_id: int, until_date: float = time.time()) -> bool:
        '''Выгоняет пользователя из чата'''
        method = 'kickChatMember'
        if chat_id is None:
            raise ValueError("chat_id не может быть None")
        if user_id is None:
            raise ValueError("user_id не может быть None")
        params = {
            'chat_id': chat_id,
            'user_id': user_id,
            'until_date': until_date}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def ban_chat_member(self, chat_id: Union[int, str], user_id: int, until_date: float = time.time(), revoke_messages: bool = False) -> bool:
        '''Блокирует пользователя в чате'''
        method = 'banChatMember'
        if chat_id is None:
            raise ValueError("chat_id не может быть None")
        if user_id is None:
            raise ValueError("user_id не может быть None")
        params = {
            'chat_id': chat_id,
            'user_id': user_id,
            'until_date': until_date,
            'revoke_messages': revoke_messages}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def unban_chat_member(self, chat_id: Union[int, str], user_id: int, only_if_banned: bool = False) -> bool:
        '''Разблокирует пользователя в чате'''
        method = 'unbanChatMember'
        if not chat_id:
            raise ValueError("chat_id не может быть None")
        elif not user_id:
            raise ValueError("user_id не может быть None")
        params = {'chat_id': chat_id, 'user_id': user_id, 'only_if_banned': only_if_banned}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def mute_user(self, chat_id: Union[int, str], user_id: int, duration: int = 3600) -> bool:
        '''Заблокирует отправку сообщений для пользователя в чате'''
        method = 'restrictChatMember'
        if not chat_id:
            raise ValueError("chat_id не может быть None")
        elif not user_id:
            raise ValueError("user_id не может быть None")
        permissions = ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False)
        params = {'chat_id': chat_id, 'user_id': user_id, 'permissions': permissions.to_dict()}
        if duration:
            params['until_date'] = time.time() + duration
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def unmute_user(self, chat_id: Union[int, str], user_id: int) -> bool:
        '''Разблокирует отправку сообщений для пользователя в чате'''
        method = 'restrictChatMember'
        if not chat_id:
            raise ValueError("chat_id не может быть None")
        elif not user_id:
            raise ValueError("user_id не может быть None")
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True)
        params = {'chat_id': chat_id, 'user_id': user_id, 'permissions': permissions.to_dict()}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def restrict_chat_member(self, chat_id: Union[int, str], user_id: int, permissions: ChatPermissions, until_date: float = time.time()) -> bool:
        '''Изменяет разрешения пользователя в чате'''
        method = 'restrictChatMember'
        if not chat_id:
            raise ValueError("chat_id не может быть None")
        elif not user_id:
            raise ValueError("user_id не может быть None")
        elif not permissions:
            raise ValueError("permissions не может быть None")
        params = {
            'chat_id': chat_id,
            'user_id': user_id,
            'permissions': permissions.to_dict()}
        if until_date is not None:
            params['until_date'] = until_date
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def promote_chat_member(self, chat_id: Union[int, str], user_id: int, can_change_info: bool = False, can_post_messages: bool = False, can_edit_messages: bool = False, can_delete_messages: bool = False, can_invite_users: bool = False, can_restrict_members: bool = False, can_pin_messages: bool = False, can_promote_members: bool = False) -> bool:
        '''Изменяет права пользователя в чате'''
        method = 'promoteChatMember'
        if not chat_id:
            raise ValueError("chat_id не может быть None")
        elif not user_id:
            raise ValueError("user_id не может быть None")
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
            'can_promote_members': can_promote_members}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def set_chat_permissions(self, chat_id: Union[int, str], permissions: ChatPermissions) -> bool:
        '''Устанавливает права для всех участников чата'''
        method = 'setChatPermissions'
        if not chat_id:
            raise ValueError("chat_id не может быть None")
        elif not permissions:
            raise ValueError("permissions не может быть None")
        params = {'chat_id': chat_id, 'permissions': permissions.to_dict()}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def chat_permissions(self, can_send_messages: bool = True, can_send_media_messages: bool = True, can_send_polls: bool = True, can_send_other_messages: bool = True, can_add_web_page_previews: bool = True, can_change_info: bool = False, can_invite_users: bool = True, can_pin_messages: bool = False) -> dict:
        '''Создает права участника чата для передачи в другие методы'''
        permissions = ChatPermissions(
            can_send_messages=can_send_messages,
            can_send_media_messages=can_send_media_messages,
            can_send_polls=can_send_polls,
            can_send_other_messages=can_send_other_messages,
            can_add_web_page_previews=can_add_web_page_previews,
            can_change_info=can_change_info,
            can_invite_users=can_invite_users,
            can_pin_messages=can_pin_messages)
        return permissions.to_dict()

#Регистрация хэндлеров
    def message_handler(self, func: callable = None, commands: list[str] = None, regexp: str = None, content_types: list[str] = None) -> callable:
        '''Регистрирует все сообщения разных типов'''
        def decorator(handler: callable) -> callable:
            self.handlers['message'].append({
                'function': handler,
                'func': func,
                'commands': commands,
                'regexp': re.compile(regexp) if regexp else None,
                'content_types': content_types
            })
            return handler
        return decorator

    def _handle_message(self, message_data: dict) -> None:
        '''Обработка сообщений'''
        if not message_data:
            raise ValueError("message_data не может быть None")
        message = Message.from_dict(message_data)
        chat_id = message.chat.id
        if chat_id in self.next_steps and self.next_steps[chat_id]:
            step = self.next_steps[chat_id].pop(0)
            step['callback'](message, *step['args'], **step['kwargs'])
            if not self.next_steps[chat_id]:
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

    def register_next_step_handler(self, message: Message, callback: callable, *args: list, **kwargs: dict) -> None:
        '''Регистрирует следующий обработчик для сообщения'''
        if not message:
            raise ValueError("message не может быть None")
        elif not callback:
            raise ValueError("callback не может быть None")
        chat_id = message.chat.id
        if chat_id not in self.next_steps:
            self.next_steps[chat_id] = []
        self.next_steps[chat_id].append({'callback': callback, 'args': args, 'kwargs': kwargs})

    def callback_query_handler(self, func: callable = None, data: str = None) -> callable:
        '''Регистрирует callback запросы'''
        def decorator(handler: callable) -> callable:
            self.handlers['callback_query'].append({
                'function': handler,
                'func': func,
                'data': data})
            return handler
        return decorator

    def _handle_callback_query(self, callback_query_data: dict) -> None:
        '''Обрабатывает нажатия на инлайн-кнопки'''
        if not callback_query_data:
            raise ValueError("callback_query_data не может быть None")
        callback_query = CallbackQuery(callback_query_data)
        data = callback_query.data
        for handler in self.handlers['callback_query']:
            if handler['data'] is None or handler['data'] == data:
                if handler['func'] is None or handler['func'](callback_query):
                    handler['function'](callback_query)
                    break

    def answer_callback_query(self, callback_id: str, text: str = "Что-то забыли указать", show_alert: bool = False, url: str = None, cache_time: int = 0) -> bool:
        '''Отвечает на запрос callback'''
        method = 'answerCallbackQuery'
        if not callback_id:
            raise ValueError("callback_id не должен быть None")
        params = {
            'callback_query_id': callback_id,
            'text': text,
            'show_alert': show_alert,
            'cache_time': cache_time}
        if url is not None:
            params['url'] = url
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False
    

#Блок - Нейросети
def gpt3(prompt: str) -> str:
    '''Генерация текста с помощью ChatGPT'''
    try:
        resp = requests.post(url="https://api.binjie.fun/api/generateStream", headers={"origin": "https://chat9.yqcloud.top/", "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"}, json={"prompt": prompt, "withoutContext": True, "stream": False})
        resp.encoding = "utf-8"
        if resp.status_code != 200:
            return "Что-то не так с ChatGPT"
        else:
            return resp.text
    except Exception as e:
        return "Ошибка соединения"