import requests, json, os, time, datetime, re, bs4, random, string, base64, threading
from typing import Optional, Union, BinaryIO


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
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.file_size = file_size

    @classmethod
    def from_dict(cls, data: dict) -> 'PhotoSize':
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            width=data['width'],
            height=data['height'],
            file_size=data.get('file_size'))

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

class Location:
    def __init__(self, latitude: float, longitude: float, horizontal_accuracy: float = None,
                 live_period: int = None, heading: int = None, proximity_alert_radius: int = None):
        '''Класс для представления геолокации в Telegram API'''
        self.latitude = latitude
        self.longitude = longitude
        self.horizontal_accuracy = horizontal_accuracy
        self.live_period = live_period
        self.heading = heading
        self.proximity_alert_radius = proximity_alert_radius

    @classmethod
    def from_dict(cls, data: dict) -> 'Location':
        '''Создает объект Location из словаря, полученного от Telegram API'''
        return cls(
            latitude=data['latitude'],
            longitude=data['longitude'],
            horizontal_accuracy=data.get('horizontal_accuracy'),
            live_period=data.get('live_period'),
            heading=data.get('heading'),
            proximity_alert_radius=data.get('proximity_alert_radius'))

    def to_dict(self) -> dict:
        '''Преобразует объект Location в словарь'''
        data = {'latitude': self.latitude, 'longitude': self.longitude}
        if self.horizontal_accuracy is not None:
            data['horizontal_accuracy'] = self.horizontal_accuracy
        if self.live_period is not None:
            data['live_period'] = self.live_period
        if self.heading is not None:
            data['heading'] = self.heading
        if self.proximity_alert_radius is not None:
            data['proximity_alert_radius'] = self.proximity_alert_radius
        return data

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

# Классы для inline‑результатов
class InlineQuery:
    def __init__(self, id: str, from_user: 'User', query: str, offset: str, chat_type: str = None, location: 'Location' = None):
        '''Создает объект InlineQuery для обработки inline-запросов'''
        self.id = id
        self.from_user = from_user
        self.query = query
        self.offset = offset
        self.chat_type = chat_type
        self.location = location

    @classmethod
    def from_dict(cls, data: dict) -> 'InlineQuery':
        '''Создает объект InlineQuery из словаря, возвращенного Telegram API'''
        from_user = User.from_dict(data['from'])
        location = Location.from_dict(data['location']) if 'location' in data else None
        return cls(
            id=data['id'],
            from_user=from_user,
            query=data['query'],
            offset=data['offset'],
            chat_type=data.get('chat_type'),
            location=location)

    def __repr__(self) -> str:
        '''Возвращает строковое представление объекта InlineQuery'''
        return f"InlineQuery(id={self.id}, from_user={self.from_user}, query={self.query}, offset={self.offset}, chat_type={self.chat_type}, location={self.location})"

class InlineQueryResult:
    def __init__(self, type: str, id: str):
        '''Создает объект InlineQueryResult для отправки inline-результатов через Telegram Bot API'''
        self.type = type
        self.id = id

    def to_dict(self) -> dict:
        '''Создает словарь с данными для отправки inline-результата'''
        return {'type': self.type, 'id': self.id}

class InlineQueryResultArticle(InlineQueryResult):
    def __init__(self, id: str, title: str, input_message_content: dict,
                 reply_markup: dict = None, url: str = None, hide_url: bool = None,
                 description: str = None, thumb_url: str = None, thumb_width: int = None, thumb_height: int = None):
        '''Создает объект InlineQueryResultArticle для отправки статей через Telegram Bot API'''
        super().__init__('article', id)
        self.title = title
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup
        self.url = url
        self.hide_url = hide_url
        self.description = description
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    def to_dict(self) -> dict:
        '''Создает словарь с данными для отправки статьи'''
        data = super().to_dict()
        data.update({
            'title': self.title,
            'input_message_content': self.input_message_content,
        })
        if self.reply_markup is not None:
            data['reply_markup'] = self.reply_markup
        if self.url is not None:
            data['url'] = self.url
        if self.hide_url is not None:
            data['hide_url'] = self.hide_url
        if self.description is not None:
            data['description'] = self.description
        if self.thumb_url is not None:
            data['thumb_url'] = self.thumb_url
        if self.thumb_width is not None:
            data['thumb_width'] = self.thumb_width
        if self.thumb_height is not None:
            data['thumb_height'] = self.thumb_height
        return data

class InlineQueryResultPhoto(InlineQueryResult):
    def __init__(self, id: str, photo_url: str, thumb_url: str, photo_width: int = None, photo_height: int = None,
                 title: str = None, description: str = None, caption: str = None, parse_mode: str = None,
                 reply_markup: dict = None):
        '''Создает объект InlineQueryResultPhoto для отправки фото через Telegram Bot API'''
        super().__init__('photo', id)
        self.photo_url = photo_url
        self.thumb_url = thumb_url
        self.photo_width = photo_width
        self.photo_height = photo_height
        self.title = title
        self.description = description
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup

    def to_dict(self) -> dict:
        '''Создает словарь с данными для отправки фото'''
        data = super().to_dict()
        data.update({
            'photo_url': self.photo_url,
            'thumb_url': self.thumb_url
        })
        if self.photo_width is not None:
            data['photo_width'] = self.photo_width
        if self.photo_height is not None:
            data['photo_height'] = self.photo_height
        if self.title is not None:
            data['title'] = self.title
        if self.description is not None:
            data['description'] = self.description
        if self.caption is not None:
            data['caption'] = self.caption
        if self.parse_mode is not None:
            data['parse_mode'] = self.parse_mode
        if self.reply_markup is not None:
            data['reply_markup'] = self.reply_markup
        return data

class InlineQueryResultVideo(InlineQueryResult):
    def __init__(self, id: str, video_url: str, mime_type: str, thumb_url: str, title: str,
                 caption: str = None, parse_mode: str = None, video_width: int = None,
                 video_height: int = None, video_duration: int = None, description: str = None,
                 reply_markup: dict = None):
        '''Создает объект InlineQueryResultVideo для отправки видео через Telegram Bot API'''
        super().__init__('video', id)
        self.video_url = video_url
        self.mime_type = mime_type
        self.thumb_url = thumb_url
        self.title = title
        self.caption = caption
        self.parse_mode = parse_mode
        self.video_width = video_width
        self.video_height = video_height
        self.video_duration = video_duration
        self.description = description
        self.reply_markup = reply_markup

    def to_dict(self) -> dict:
        '''Создает словарь с данными для отправки видео'''
        data = super().to_dict()
        data.update({'video_url': self.video_url, 'mime_type': self.mime_type, 'thumb_url': self.thumb_url, 'title': self.title})
        if self.caption is not None:
            data['caption'] = self.caption
        if self.parse_mode is not None:
            data['parse_mode'] = self.parse_mode
        if self.video_width is not None:
            data['video_width'] = self.video_width
        if self.video_height is not None:
            data['video_height'] = self.video_height
        if self.video_duration is not None:
            data['video_duration'] = self.video_duration
        if self.description is not None:
            data['description'] = self.description
        if self.reply_markup is not None:
            data['reply_markup'] = self.reply_markup
        return data

# Классы для платежных объектов
class LabeledPrice:
    def __init__(self, label: str, amount: int):
        '''Создает объект LabeledPrice для обработки payment-запросов в Telegram Bot API'''
        self.label = label
        self.amount = amount

    def to_dict(self) -> dict:
        '''Возвращает словарь, представляющий объект LabeledPrice'''
        return {'label': self.label, 'amount': self.amount}

class ShippingOption:
    def __init__(self, id: str, title: str, prices: list):
        '''Создает объект ShippingOption для обработки shipping-запросов в Telegram Bot API'''
        self.id = id
        self.title = title
        self.prices = prices

    def to_dict(self) -> dict:
        '''Возвращает словарь, представляющий объект ShippingOption'''
        return {'id': self.id, 'title': self.title, 'prices': [price.to_dict() for price in self.prices]}

# Класс для обработки фотографий пользователя
class UserProfilePhotos:
    def __init__(self, total_count: int, photos: list[list['PhotoSize']]):
        '''Инициализирует объект UserProfilePhotos'''
        self.total_count = total_count
        self.photos = photos

    @classmethod
    def from_dict(cls, data: dict) -> 'UserProfilePhotos':
        '''Создает объект UserProfilePhotos из словаря, полученного от Telegram API'''
        photos = [[PhotoSize.from_dict(photo) for photo in photo_list] for photo_list in data['photos']]
        return cls(total_count=data['total_count'], photos=photos)

    def get_photo_id(self, index: int = -1) -> Optional[str]:
        '''Возвращает file_id фотографии по указанному индексу'''
        if not self.photos:
            return None
        if index == -1:
            index = len(self.photos) - 1
        if 0 <= index < len(self.photos):
            return self.photos[index][-1].file_id
        else:
            raise IndexError("Индекс выходит за пределы списка фотографий")

# Классы для обработки callback-запросов
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
                 caption: str = None, new_chat_members: list = None, new_chat_member: 'User' = None, 
                 left_chat_member: 'User' = None, entities: list = None):
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
        self.caption = caption
        self.new_chat_members = new_chat_members
        self.new_chat_member = new_chat_member
        self.left_chat_member = left_chat_member
        self.entities = entities

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
        caption = data.get('caption')
        entities = [MessageEntity(**entity) for entity in data.get('entities', [])]
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
            caption=caption,
            new_chat_members=new_chat_members,
            new_chat_member=new_chat_member,
            left_chat_member=left_chat_member,
            entities=entities)


#Основа
class Bot:
    def __init__(self, token):
        '''Создает экземпляр Bot'''
        self.token = token
        self.handlers = {'message': [], 'command': [], 'callback_query': [], 'inline_query': []}
        self.running = False
        self.update_offset = 0
        self.next_steps = {}
        self.bot_info = self.get_me()
        self.bot_username = self.bot_info.username.lower() if self.bot_info and self.bot_info.username else None

    def _make_request(self, method, params=None, files=None, json=None):
        '''Отправляет запрос в Telegram API с обработкой всех ошибок и повторными попытками'''
        url = f'https://api.telegram.org/bot{self.token}/{method}'
        max_retries = 3
        retry_after = 3
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
                return None
            except Exception as e:
                print(f"Необработанная ошибка: {e}")
                return None
            time.sleep(2 ** attempt + random.uniform(0, 1))
        print(f"Не удалось выполнить запрос {method} после {max_retries} попыток")
        return None

    def reply_message(self, chat_id: Union[int, str] = None, text: str = None, mode: str = "Markdown", disable_web_page_preview: bool = None, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''
        Отправляет сообщение.

        :param chat_id: Идентификатор чата, куда отправляется сообщение.
        :type chat_id: Union[int, str], optional
        :param text: Текст сообщения.
        :type text: str, optional
        :param mode: Режим форматирования текста (например, "Markdown" или "HTML").
        :type mode: str, optional
        :param disable_web_page_preview: Отключает предпросмотр ссылок.
        :type disable_web_page_preview: bool, optional
        :param disable_notification: Отключает уведомление о сообщении.
        :type disable_notification: bool, optional
        :param reply_to_message_id: ID сообщения, на которое отвечает это сообщение.
        :type reply_to_message_id: int, optional
        :param reply_markup: Дополнительная клавиатура или разметка (в формате словаря или объекта Markup).
        :type reply_markup: Union[dict, Markup], optional
        :return: Объект Message при успехе, None при неудаче.
        :rtype: Optional[Message]
        '''
        method = 'sendMessage'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif text is None:
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

    def reply_photo(self, chat_id: Union[int, str] = None, photo: Union[str, bytes] = None, caption: str = None, mode: str = "Markdown", disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''
        Отправляет фотографию.

        :param chat_id: Идентификатор чата, куда отправляется фото.
        :type chat_id: int or str
        :param photo: Путь к файлу, URL или байты фотографии.
        :type photo: str or bytes
        :param caption: Подпись к фотографии.
        :type caption: str, optional
        :param mode: Режим форматирования подписи ('Markdown' или 'HTML').
        :type mode: str, optional
        :param disable_notification: Отключить уведомление о сообщении.
        :type disable_notification: bool, optional
        :param reply_to_message_id: Идентификатор сообщения, на которое отвечаем.
        :type reply_to_message_id: int, optional
        :param reply_markup: Клавиатура или разметка для сообщения.
        :type reply_markup: dict or Markup, optional
        :return: Объект Message, если фото отправлено успешно, иначе None.
        :rtype: Message or None
        :raises ValueError: Если chat_id или photo не указаны.
        '''
        method = 'sendPhoto'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif photo is None:
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

    def reply_audio(self, chat_id: Union[int, str] = None, audio: Union[str, bytes] = None, caption: str = None, mode: str = "Markdown", duration: int = None, performer: str = None, title: str = None, thumb: Union[str, bytes] = None, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''
        Отправляет аудиофайл.

        :param chat_id: Идентификатор чата, куда отправляется аудио.
        :type chat_id: int or str
        :param audio: Путь к аудиофайлу, URL или байты.
        :type audio: str or bytes
        :param caption: Подпись к аудио.
        :type caption: str, optional
        :param mode: Режим форматирования подписи ('Markdown' или 'HTML').
        :type mode: str, optional
        :param duration: Длительность аудио в секундах.
        :type duration: int, optional
        :param performer: Исполнитель аудио.
        :type performer: str, optional
        :param title: Название аудио.
        :type title: str, optional
        :param thumb: Миниатюра аудио (путь к файлу, URL или байты).
        :type thumb: str or bytes, optional
        :param disable_notification: Отключить уведомление о сообщении.
        :type disable_notification: bool, optional
        :param reply_to_message_id: Идентификатор сообщения, на которое отвечаем.
        :type reply_to_message_id: int, optional
        :param reply_markup: Клавиатура или разметка для сообщения.
        :type reply_markup: dict or Markup, optional
        :return: Объект Message, если аудио отправлено успешно, иначе None.
        :rtype: Message or None
        :raises ValueError: Если chat_id или audio не указаны.
        '''
        method = 'sendAudio'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif audio is None:
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

    def reply_document(self, chat_id: Union[int, str] = None, document: Union[str, bytes] = None, caption: str = None, mode: str = "Markdown", disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''
        Отправляет документ.

        :param chat_id: Идентификатор чата, куда отправляется документ.
        :type chat_id: int or str
        :param document: Путь к документу, URL или байты.
        :type document: str or bytes
        :param caption: Подпись к документу.
        :type caption: str, optional
        :param mode: Режим форматирования подписи ('Markdown' или 'HTML').
        :type mode: str, optional
        :param disable_notification: Отключить уведомление о сообщении.
        :type disable_notification: bool, optional
        :param reply_to_message_id: Идентификатор сообщения, на которое отвечаем.
        :type reply_to_message_id: int, optional
        :param reply_markup: Клавиатура или разметка для сообщения.
        :type reply_markup: dict or Markup, optional
        :return: Объект Message, если документ отправлен успешно, иначе None.
        :rtype: Message or None
        :raises ValueError: Если chat_id или document не указаны.
        '''
        method = 'sendDocument'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif document is None:
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

    def reply_video(self, chat_id: Union[int, str] = None, video: Union[str, bytes] = None, duration: int = None, width: int = None, height: int = None, caption: str = None, mode: str = "Markdown", supports_streaming: bool = None, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''
        Отправляет видеофайл.

        :param chat_id: Идентификатор чата, куда отправляется видео.
        :type chat_id: int or str
        :param video: Путь к видеофайлу, URL или байты.
        :type video: str or bytes
        :param caption: Подпись к видео.
        :type caption: str, optional
        :param mode: Режим форматирования подписи ('Markdown' или 'HTML').
        :type mode: str, optional
        :param duration: Длительность видео в секундах.
        :type duration: int, optional
        :param width: Ширина видео в пикселях.
        :type width: int, optional
        :param height: Высота видео в пикселях.
        :type height: int, optional
        :param thumb: Миниатюра видео (путь к файлу, URL или байты).
        :type thumb: str or bytes, optional
        :param disable_notification: Отключить уведомление о сообщении.
        :type disable_notification: bool, optional
        :param reply_to_message_id: Идентификатор сообщения, на которое отвечаем.
        :type reply_to_message_id: int, optional
        :param reply_markup: Клавиатура или разметка для сообщения.
        :type reply_markup: dict or Markup, optional
        :return: Объект Message, если видео отправлено успешно, иначе None.
        :rtype: Message or None
        :raises ValueError: Если chat_id или video не указаны.
        '''
        method = 'sendVideo'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif video is None:
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

    def reply_video_note(self, chat_id: Union[int, str] = None, video_note: Union[str, bytes] = None, duration: int = None, length: int = None, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''
        Отправляет видео кружочек.

        :param chat_id: Идентификатор чата, куда отправляется видео.
        :type chat_id: int or str
        :param video_note: Путь к видеофайлу, URL или байты.
        :type video_note: str or bytes
        :param duration: Длительность видео в секундах.
        :type duration: int, optional
        :param length: Длительность видео в секундах.
        :type length: int, optional
        :param disable_notification: Отключить уведомление о сообщении.
        :type disable_notification: bool, optional
        :param reply_to_message_id: Идентификатор сообщения, на которое отвечаем.
        :type reply_to_message_id: int, optional
        :param reply_markup: Клавиатура или разметка для сообщения.
        :type reply_markup: dict or Markup, optional
        :return: Объект Message, если видео отправлено успешно, иначе None.
        :rtype: Message or None
        :raises ValueError: Если chat_id или video_note не указаны.
        '''
        method = 'sendVideoNote'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif video_note is None:
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

    def reply_animation(self, chat_id: Union[int, str] = None, animation: Union[str, bytes] = None, duration: int = None, width: int = None, height: int = None, caption: str = None, mode: str = "Markdown", disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''
        Отправляет анимацию.

        :param chat_id: Идентификатор чата, куда отправляется анимация.
        :type chat_id: int or str
        :param animation: Путь к анимационному файлу, URL или байты.
        :type animation: str or bytes
        :param duration: Длительность анимации в секундах.
        :type duration: int, optional
        :param width: Ширина анимации.
        :type width: int, optional
        :param height: Высота анимации.
        :type height: int, optional
        :param caption: Текст описания анимации.
        :type caption: str, optional
        :param mode: Режим разметки текста.
        :type mode: str, optional
        :param disable_notification: Отключить уведомление о сообщении.
        :type disable_notification: bool, optional
        :param reply_to_message_id: Идентификатор сообщения, на которое отвечаем.
        :type reply_to_message_id: int, optional
        :param reply_markup: Клавиатура или разметка для сообщения.
        :type reply_markup: dict or Markup, optional
        :return: Объект Message, если анимация отправлена успешно, иначе None.
        :rtype: Message or None
        :raises ValueError: Если chat_id или animation не указаны.
        '''
        method = 'sendAnimation'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif animation is None:
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

    def reply_voice(self, chat_id: Union[int, str] = None, voice: Union[str, bytes] = None, caption: str = None, mode: str = "Markdown", duration: int = None, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''
        Отправляет голосовое сообщение.

        :param chat_id: Идентификатор чата, куда отправляется голосовое сообщение.
        :type chat_id: int or str
        :param voice: Путь к голосовому файлу, URL или байты.
        :type voice: str or bytes
        :param caption: Текст описания голосового сообщения.
        :type caption: str, optional
        :param mode: Режим разметки текста.
        :type mode: str, optional
        :param duration: Длительность голосового сообщения в секундах.
        :type duration: int, optional
        :param disable_notification: Отключить уведомление о сообщении.
        :type disable_notification: bool, optional
        :param reply_to_message_id: Идентификатор сообщения, на которое отвечаем.
        :type reply_to_message_id: int, optional
        :param reply_markup: Клавиатура или разметка для сообщения.
        :type reply_markup: dict or Markup, optional
        :return: Объект Message, если голосовое сообщение отправлено успешно, иначе None.
        :rtype: Message or None
        :raises ValueError: Если chat_id или voice не указаны.
        '''
        method = 'sendVoice'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif voice is None:
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

    def reply_location(self, chat_id: Union[int, str] = None, latitude: float = None, longitude: float = None, live_period: int = None, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''
        Отправляет локацию.

        :param chat_id: Идентификатор чата, куда отправляется локация.
        :type chat_id: int or str
        :param latitude: Широта.
        :type latitude: float
        :param longitude: Долгота.
        :type longitude: float
        :param live_period: Период обновления локации в секундах.
        :type live_period: int, optional
        :param disable_notification: Отключить уведомление о сообщении.
        :type disable_notification: bool, optional
        :param reply_to_message_id: Идентификатор сообщения, на которое отвечаем.
        :type reply_to_message_id: int, optional
        :param reply_markup: Клавиатура или разметка для сообщения.
        :type reply_markup: dict or Markup, optional
        :return: Объект Location, если локация отправлена успешно, иначе None.
        :rtype: Location or None
        :raises ValueError: Если chat_id, latitude или longitude не указаны.
        '''
        method = 'sendLocation'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif latitude is None:
            raise ValueError("latitude не должен быть None")
        elif longitude is None:
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
            return Location.from_dict(response['result'])
        else:
            return None

    def reply_chat_action(self, chat_id: Union[int, str] = None, action: str = None) -> bool:
        '''
        Отправляет активность.

        :param chat_id: Идентификатор чата.
        :type chat_id: int or str
        :param action: Тип активности.
        :type action: str
        :return: True, если активность отправлена успешно, иначе False.
        :rtype: bool
        :raises ValueError: Если chat_id или action не указаны.
        '''
        method = 'sendChatAction'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif action is None:
            raise ValueError("action не должен быть None")
        params = {'chat_id': chat_id, 'action': action}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False
    
    def reply_venue(self, chat_id: Union[int, str] = None, latitude: float = None, longitude: float = None, title: str = None, address: str = None, foursquare_id: str = None, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''
        Отправляет место.

        :param chat_id: Идентификатор чата, куда отправляется место.
        :type chat_id: int or str
        :param latitude: Широта.
        :type latitude: float
        :param longitude: Долгота.
        :type longitude: float
        :param title: Название места.
        :type title: str
        :param address: Адрес места.
        :type address: str
        :param foursquare_id: Идентификатор Foursquare.
        :type foursquare_id: str
        :param disable_notification: Отключить уведомление о сообщении.
        :type disable_notification: bool, optional
        :param reply_to_message_id: Идентификатор сообщения, на которое отвечаем.
        :type reply_to_message_id: int, optional
        :param reply_markup: Клавиатура или разметка для сообщения.
        :type reply_markup: dict or Markup, optional
        :return: Объект Message, если место отправлено успешно, иначе None.
        :rtype: Message or None
        :raises ValueError: Если chat_id, latitude, longitude, title или address не указаны.
        '''
        method = 'sendVenue'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif latitude is None:
            raise ValueError("latitude не должен быть None")
        elif longitude is None:
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
    
    def reply_contact(self, chat_id: Union[int, str] = None, phone_number: str = None, first_name: str = None, last_name: str = None, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''
        Отправляет контакт.

        :param chat_id: Идентификатор чата, куда отправляется контакт.
        :type chat_id: int or str
        :param phone_number: Номер телефона.
        :type phone_number: str
        :param first_name: Имя.
        :type first_name: str
        :param last_name: Фамилия.
        :type last_name: str
        :param disable_notification: Отключить уведомление о сообщении.
        :type disable_notification: bool, optional
        :param reply_to_message_id: Идентификатор сообщения, на которое отвечаем.
        :type reply_to_message_id: int, optional
        :param reply_markup: Клавиатура или разметка для сообщения.
        :type reply_markup: dict or Markup, optional
        :return: Объект Message, если контакт отправлен успешно, иначе None.
        :rtype: Message or None
        :raises ValueError: Если chat_id, phone_number или first_name не указаны.
        '''
        method = 'sendContact'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif phone_number is None:
            raise ValueError("phone_number не должен быть None")
        elif first_name is None:
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
    
    def reply_sticker(self, chat_id: Union[int, str] = None, sticker: Union[str, bytes] = None, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''
        Отправляет стикер.

        :param chat_id: Идентификатор чата, куда отправляется стикер.
        :type chat_id: int or str
        :param sticker: Идентификатор стикера или файл стикера.
        :type sticker: str or bytes
        :param disable_notification: Отключить уведомление о сообщении.
        :type disable_notification: bool, optional
        :param reply_to_message_id: Идентификатор сообщения, на которое отвечаем.
        :type reply_to_message_id: int, optional
        :param reply_markup: Клавиатура или разметка для сообщения.
        :type reply_markup: dict or Markup, optional
        :return: Объект Message, если стикер отправлен успешно, иначе None.
        :rtype: Message or None
        :raises ValueError: Если chat_id или sticker не указаны.
        '''
        method = 'sendSticker'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif sticker is None:
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
        
    def reply_dice(self, chat_id: Union[int, str] = None, emoji: str = None, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''
        Отправляет большие эмодзи.

        :param chat_id: Идентификатор чата, куда отправляется эмодзи.
        :type chat_id: int or str
        :param emoji: Эмодзи.
        :type emoji: str
        :param disable_notification: Отключить уведомление о сообщении.
        :type disable_notification: bool, optional
        :param reply_to_message_id: Идентификатор сообщения, на которое отвечаем.
        :type reply_to_message_id: int, optional
        :param reply_markup: Клавиатура или разметка для сообщения.
        :type reply_markup: dict or Markup, optional
        :return: True, если эмодзи отправлен успешно, иначе False.
        :rtype: bool
        :raises ValueError: Если chat_id или emoji не указаны.
        '''
        method = 'sendDice'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif emoji is None:
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

    def reply_message_reaction(self, chat_id: Union[int, str] = None, message_id: int = None, reaction: str = None, is_big: bool = False) -> bool:
        '''
        Отправить реакцию.

        :param chat_id: Идентификатор чата, куда отправляется реакция.
        :type chat_id: int or str
        :param message_id: Идентификатор сообщения, на которое отправляется реакция.
        :type message_id: int
        :param reaction: Реакция.
        :type reaction: str
        :param is_big: Размер реакции.
        :type is_big: bool, optional
        :return: True, если реакция отправлена успешно, иначе False.
        :rtype: bool
        :raises ValueError: Если chat_id или message_id или reaction не указаны.
        '''
        method = 'setMessageReaction'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif message_id is None:
            raise ValueError("message_id не должен быть None")
        elif reaction is None:
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

    def reply_invoice(self, chat_id: Union[int, str] = None, title: str = None, description: str = None, payload: str = None,
                     provider_token: str = None, currency: str = None, prices: list = None, max_tip_amount: int = None,
                     suggested_tip_amounts: list = None, start_parameter: str = None, provider_data: str = None,
                     photo_url: str = None, photo_size: int = None, photo_width: int = None, photo_height: int = None,
                     need_name: bool = None, need_phone_number: bool = None, need_email: bool = None,
                     need_shipping_address: bool = None, send_phone_number_to_provider: bool = None,
                     send_email_to_provider: bool = None, is_flexible: bool = None, disable_notification: bool = None,
                     reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''
        Отправляет счет на оплату.

        :param chat_id: Идентификатор чата, куда отправляется счет.
        :type chat_id: int or str
        :param title: Заголовок счета.
        :type title: str
        :param description: Описание счета.
        :type description: str
        :param payload: Данные счета.
        :type payload: str
        :param provider_token: Токен провайдера.
        :type provider_token: str
        :param currency: Валюта счета.
        :type currency: str
        :param prices: Список цен.
        :type prices: list
        :param max_tip_amount: Максимальная сумма подсказки.
        :type max_tip_amount: int, optional
        :param suggested_tip_amounts: Список подсказок.
        :type suggested_tip_amounts: list, optional
        :param start_parameter: Стартовый параметр.
        :type start_parameter: str, optional
        :param provider_data: Данные провайдера.
        :type provider_data: str, optional
        :param photo_url: URL фотографии.
        :type photo_url: str, optional
        :param photo_size: Размер фотографии.
        :type photo_size: int, optional
        :param photo_width: Ширина фотографии.
        :type photo_width: int, optional
        :param photo_height: Высота фотографии.
        :type photo_height: int, optional
        :param need_name: Нужно ли запрашивать имя.
        :type need_name: bool, optional
        :param need_phone_number: Нужно ли запрашивать номер телефона.
        :type need_phone_number: bool, optional
        :param need_email: Нужно ли запрашивать email.
        :type need_email: bool, optional
        :param need_shipping_address: Нужно ли запрашивать адрес доставки.
        :type need_shipping_address: bool, optional
        :param send_phone_number_to_provider: Отправлять номер телефона провайдеру.
        :type send_phone_number_to_provider: bool, optional
        :param send_email_to_provider: Отправлять email провайдеру.
        :type send_email_to_provider: bool, optional
        :param is_flexible: Гибкий счет.
        :type is_flexible: bool, optional
        :param disable_notification: Отключить уведомление.
        :type disable_notification: bool, optional
        :param reply_to_message_id: Идентификатор сообщения-ответа.
        :type reply_to_message_id: int, optional
        :param reply_markup: Клавиатура или разметка для сообщения.
        :type reply_markup: dict or Markup, optional
        :return: Объект сообщения.
        :rtype: Message
        '''
        method = 'sendInvoice'
        if chat_id is None or title is None or description is None or payload is None or provider_token is None or currency is None or prices is None:
            raise ValueError("Отсутствуют обязательные параметры для отправки инвойса")
        if prices and hasattr(prices[0], 'to_dict'):
            prices_serialized = json.dumps([price.to_dict() for price in prices])
        else:
            prices_serialized = json.dumps(prices)
        params = {
            'chat_id': chat_id,
            'title': title,
            'description': description,
            'payload': payload,
            'provider_token': provider_token,
            'currency': currency,
            'prices': prices_serialized,
            'max_tip_amount': max_tip_amount,
            'suggested_tip_amounts': json.dumps(suggested_tip_amounts) if suggested_tip_amounts is not None else None,
            'start_parameter': start_parameter,
            'provider_data': provider_data,
            'photo_url': photo_url,
            'photo_size': photo_size,
            'photo_width': photo_width,
            'photo_height': photo_height,
            'need_name': need_name,
            'need_phone_number': need_phone_number,
            'need_email': need_email,
            'need_shipping_address': need_shipping_address,
            'send_phone_number_to_provider': send_phone_number_to_provider,
            'send_email_to_provider': send_email_to_provider,
            'is_flexible': is_flexible,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        return None

    def reply_shipping_query(self, shipping_query_id: str = None, ok: bool = None, shipping_options: list = None,
                                error_message: str = None) -> bool:
        '''
        Отвечает на запрос доставки.

        :param shipping_query_id: Идентификатор запроса доставки.
        :type shipping_query_id: str, optional
        :param ok: Ответ.
        :type ok: bool, optional
        :param shipping_options: Опции доставки.
        :type shipping_options: list, optional
        :param error_message: Сообщение об ошибке.
        :type error_message: str, optional
        :return: True, если запрос обработан, False в противном случае.
        :rtype: bool
        '''
        method = 'answerShippingQuery'
        if shipping_query_id is None or ok is None:
            raise ValueError("shipping_query_id и ok обязательны")
        if shipping_options and hasattr(shipping_options[0], 'to_dict'):
            shipping_options_serialized = json.dumps([option.to_dict() for option in shipping_options])
        else:
            shipping_options_serialized = json.dumps(shipping_options) if shipping_options is not None else None
        params = {
            'shipping_query_id': shipping_query_id,
            'ok': ok,
            'shipping_options': shipping_options_serialized,
            'error_message': error_message}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def reply_pre_checkout_query(self, pre_checkout_query_id: str = None, ok: bool = None,
                                  error_message: str = None) -> bool:
        '''
        Отвечает на запрос предчекаута.

        :param pre_checkout_query_id: Идентификатор предчекаута.
        :type pre_checkout_query_id: str, optional
        :param ok: Ответ.
        :type ok: bool, optional
        :param error_message: Сообщение об ошибке.
        :type error_message: str, optional
        :return: True, если запрос обработан, False в противном случае.
        :rtype: bool
        '''
        method = 'answerPreCheckoutQuery'
        if pre_checkout_query_id is None or ok is None:
            raise ValueError("pre_checkout_query_id и ok обязательны")
        params = {
            'pre_checkout_query_id': pre_checkout_query_id,
            'ok': ok,
            'error_message': error_message}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def reply_poll(self, chat_id: Union[int, str] = None, question: str = None, options: list = None, is_anonymous: bool = False, type: str = 'regular', allows_multiple_answers: bool = False, correct_option_id: int = None, explanation: str = None, mode: str = "Markdown", open_period: int = None, close_date: int = None, is_closed: bool = False, disable_notification: bool = None, reply_to_message_id: int = None, reply_markup: Union[dict, Markup] = None) -> bool:
        '''
        Отправляет опрос.

        :param chat_id: Идентификатор чата.
        :type chat_id: int or str, optional
        :param question: Текст вопроса.
        :type question: str, optional
        :param options: Опции опроса.
        :type options: list, optional
        :param is_anonymous: Анонимность опроса.
        :type is_anonymous: bool, optional
        :param type: Тип опроса.
        :type type: str, optional
        :param allows_multiple_answers: Разрешить несколько ответов.
        :type allows_multiple_answers: bool, optional
        :param correct_option_id: Идентификатор правильного ответа.
        :type correct_option_id: int, optional
        :param explanation: Текст объяснения.
        :type explanation: str, optional
        :param mode: Режим объяснения.
        :type mode: str, optional
        :param open_period: Длительность опроса в секундах.
        :type open_period: int, optional
        :param close_date: Дата закрытия опроса.
        :type close_date: int, optional
        :param is_closed: Закрыт ли опрос.
        :type is_closed: bool, optional
        :param disable_notification: Отключить уведомление.
        :type disable_notification: bool, optional
        :param reply_to_message_id: Идентификатор сообщения для ответа.
        :type reply_to_message_id: int, optional
        :param reply_markup: Клавиатура или разметка для сообщения.
        :type reply_markup: dict or Markup, optional
        :return: True, если опрос отправлен, False в противном случае.
        :rtype: bool
        '''
        method = 'sendPoll'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif question is None:
            raise ValueError("question не должен быть None")
        elif options is None:
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

    def stop_poll(self, chat_id: Union[int, str] = None, message_id: int = None, reply_markup: Union[dict, Markup] = None) -> bool:
        '''
        Завершает активный опрос в чате.

        :param chat_id: Идентификатор чата.
        :type chat_id: int or str, optional
        :param message_id: Идентификатор сообщения опроса.
        :type message_id: int, optional
        :param reply_markup: Клавиатура или разметка для сообщения.
        :type reply_markup: dict or Markup, optional
        :return: True, если опрос завершен, False в противном случае.
        :rtype: bool
        '''
        method = 'stopPoll'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif message_id is None:
            raise ValueError("message_id не должен быть None")
        params = {'chat_id': chat_id, 'message_id': message_id, 'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False
        
    def pin_message(self, chat_id: Union[int, str] = None, message_id: int = None) -> bool:
        '''
        Закрепляет сообщение в чате.

        :param chat_id: Идентификатор чата.
        :type chat_id: int or str, optional
        :param message_id: Идентификатор сообщения.
        :type message_id: int, optional
        :return: True, если сообщение закреплено, False в противном случае.
        :rtype: bool
        '''
        method = 'pinChatMessage'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif message_id is None:
            raise ValueError("message_id не должен быть None")
        params = {'chat_id': chat_id, 'message_id': message_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def unpin_message(self, chat_id: Union[int, str] = None, message_id: int = None) -> bool:
        '''
        Открепляет сообщение в чате.

        :param chat_id: Идентификатор чата.
        :type chat_id: int or str, optional
        :param message_id: Идентификатор сообщения.
        :type message_id: int, optional
        :return: True, если сообщение откреплено, False в противном случае.
        :rtype: bool
        '''
        method = 'unpinChatMessage'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif message_id is None:
            raise ValueError("message_id не должен быть None")
        params = {'chat_id': chat_id, 'message_id': message_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def forward_message(self, chat_id: Union[int, str] = None, from_chat_id: Union[int, str] = None, message_id: int = None, disable_notification: bool = None) -> bool:
        '''
        Пересылает сообщение.

        :param chat_id: Идентификатор чата, в который нужно переслать сообщение.
        :type chat_id: int or str, optional
        :param from_chat_id: Идентификатор чата, из которого нужно переслать сообщение.
        :type from_chat_id: int or str, optional
        :param message_id: Идентификатор сообщения, которое нужно переслать.
        :type message_id: int, optional
        :param disable_notification: Отключить уведомление о пересланном сообщении.
        :type disable_notification: bool, optional
        :return: True, если сообщение переслано, False в противном случае.
        :rtype: bool
        '''
        method = 'forwardMessage'
        if chat_id:
            raise ValueError("chat_id не должен быть None")
        elif from_chat_id is None:
            raise ValueError("from_chat_id не должен быть None")
        elif message_id is None:
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
    
    def forward_messages(self, chat_id: Union[int, str] = None, from_chat_id: Union[int, str] = None, message_ids: Union[int, list] = None, disable_notification: bool = None) -> bool:
        '''
        Пересылает несколько сообщений.

        :param chat_id: Идентификатор чата, в который нужно переслать сообщения.
        :type chat_id: int or str, optional
        :param from_chat_id: Идентификатор чата, из которого нужно переслать сообщения.
        :type from_chat_id: int or str, optional
        :param message_ids: Список идентификаторов сообщений, которые нужно переслать.
        :type message_ids: int or list, optional
        :param disable_notification: Отключить уведомление о пересланном сообщении.
        :type disable_notification: bool, optional
        :return: True, если сообщения пересланы, False в противном случае.
        :rtype: bool
        '''
        method = 'forwardMessages'
        if chat_id:
            raise ValueError("chat_id не должен быть None")
        elif from_chat_id is None:
            raise ValueError("from_chat_id не должен быть None")
        elif message_ids is None:
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

    def copy_message(self, chat_id: Union[int, str] = None, from_chat_id: Union[int, str] = None, message_id: int = None, caption: str = None, disable_notification: bool = None, mode: str = "Markdown", reply_markup: Union[dict, Markup] = None) -> bool:
        '''
        Копирует сообщение.

        :param chat_id: Идентификатор чата, в который нужно скопировать сообщение.
        :type chat_id: int or str, optional
        :param from_chat_id: Идентификатор чата, из которого нужно скопировать сообщение.
        :type from_chat_id: int or str, optional
        :param message_id: Идентификатор сообщения, которое нужно скопировать.
        :type message_id: int, optional
        :param caption: Текст, который нужно добавить к скопированному сообщению.
        :type caption: str, optional
        :param disable_notification: Отключить уведомление о скопированном сообщении.
        :type disable_notification: bool, optional
        :param mode: Режим разметки.
        :type mode: str, optional
        :param reply_markup: Объект разметки, которая будет добавлена к скопированному сообщению.
        :type reply_markup: dict or Markup, optional
        :return: True, если сообщение скопировано, False в противном случае.
        :rtype: bool
        '''
        method = 'copyMessage'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif from_chat_id is None:
            raise ValueError("from_chat_id не должен быть None")
        elif message_id is None:
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
    
    def copy_messages(self, chat_id: Union[int, str] = None, from_chat_id: Union[int, str] = None, message_ids: Union[int, list] = None, disable_notification: bool = None) -> bool:
        '''
        Копирует несколько сообщений.

        :param chat_id: Идентификатор чата, в который нужно скопировать сообщения.
        :type chat_id: int or str, optional
        :param from_chat_id: Идентификатор чата, из которого нужно скопировать сообщения.
        :type from_chat_id: int or str, optional
        :param message_ids: Список идентификаторов сообщений, которые нужно скопировать.
        :type message_ids: int or list, optional
        :param disable_notification: Отключить уведомление о скопированных сообщениях.
        :type disable_notification: bool, optional
        :return: True, если сообщения скопированы, False в противном случае.
        :rtype: bool
        '''
        method = 'copyMessages'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif from_chat_id is None:
            raise ValueError("from_chat_id не должен быть None")
        elif message_ids is None:
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

    def delete_message(self, chat_id: Union[int, str] = None, message_id: int = None) -> bool:
        '''
        Удаляет сообщение.

        :param chat_id: Идентификатор чата, в котором нужно удалить сообщение.
        :type chat_id: int or str, optional
        :param message_id: Идентификатор сообщения, которое нужно удалить.
        :type message_id: int, optional
        :return: True, если сообщение удалено, False в противном случае.
        :rtype: bool
        '''
        method = 'deleteMessage'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif message_id is None:
            raise ValueError("message_id не должен быть None")
        params = {'chat_id': chat_id, 'message_id': message_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def delete_messages(self, chat_id: Union[int, str] = None, message_ids: Union[int, list] = None) -> bool:
        '''
        Удаляет несколько сообщений.

        :param chat_id: Идентификатор чата, в котором нужно удалить сообщения.
        :type chat_id: int or str, optional
        :param message_ids: Список идентификаторов сообщений, которые нужно удалить или одиночный ID.
        :type message_ids: int or list, optional
        :return: True, если все сообщения удалены успешно, False в противном случае.
        :rtype: bool
        '''
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        if message_ids is None:
            raise ValueError("message_ids не должен быть None")
        if isinstance(message_ids, int):
            message_ids = [message_ids]
        elif not isinstance(message_ids, list):
            raise ValueError("message_ids должен быть int или list")
        success = True
        for message_id in message_ids:
            try:
                self.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {str(e)}")
                success = False
        return success

    def get_profile_photos(self, user_id: int = None, offset: int = None, limit: int = None) -> Optional['UserProfilePhotos']:
        '''
        Получает объект UserProfilePhotos, содержащий фотографии профиля пользователя.

        :param user_id: Идентификатор пользователя
        :type user_id: int
        :param offset: Смещение для получения фотографий
        :type offset: int
        :param limit: Максимальное количество фотографий для получения
        :type limit: int

        :return: Объект фотографий пользователя.
        :rtype: UserProfilePhotos
        '''
        if user_id is None:
            raise ValueError("user_id не должен быть None")
        method_url = 'getUserProfilePhotos'
        params = {'user_id': user_id, 'offset': offset, 'limit': limit}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method_url, params=params)
        if response and 'result' in response:
            return UserProfilePhotos.from_dict(response['result'])
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

    def get_file(self, file_id: str = None) -> Optional['File']:
        '''Получает информацию о файле на серверах Telegram'''
        method = 'getFile'
        if file_id is None:
            raise ValueError("file_id не может быть None")
        params = {'file_id': file_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return File.from_dict(response['result'])
        else:
            return None

    def download_file(self, file: str = None, save_path: str = None, chunk_size: int = 1024, timeout: int = 60, headers: dict = None, stream: bool = True) -> bool:
        '''Скачивает файл с серверов Telegram и сохраняет'''
        if file is None:
            raise ValueError("file не должен быть None")
        elif not isinstance(file, File):
            raise ValueError("file должен быть объектом класса TelegramFile")
        elif file.file_path is None:
            raise ValueError("file_path не должен быть None")
        elif save_path is None:
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
    def edit_message_text(self, chat_id: Union[int, str] = None, message_id: int = None, text: str = None, inline_message_id: str = None, mode="Markdown", reply_markup: Union[dict, Markup] = None) -> bool:
        '''Редактирует текст сообщения'''
        method = 'editMessageText'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif message_id is None:
            raise ValueError("message_id не должен быть None")
        elif text is None:
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

    def edit_message_caption(self, chat_id: Union[int, str] = None, message_id: int = None, caption: str = None, inline_message_id: str = None, mode: str = "Markdown", show_caption_above_media: bool = False, reply_markup: Union[dict, Markup] = None) -> bool:
        '''Редактирует описание медиа'''
        method = 'editMessageCaption'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif message_id is None:
            raise ValueError("message_id не должен быть None")
        elif caption is None:
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

    def reply_media_group(self, chat_id: Union[int, str] = None, media: list = None, disable_notification: bool = None) -> Optional[list]:
        '''
        Отправляет несколько медиа-объектов.

        :param chat_id: Идентификатор чата, куда отправляются медиа-объекты.
        :type chat_id: int or str
        :param media: Список медиа-объектов.
        :type media: list
        :param disable_notification: Отключить уведомление о сообщении.
        :type disable_notification: bool, optional
        :return: Список объектов Message, если медиа-объекты отправлены успешно, иначе None.
        :rtype: list or None
        :raises ValueError: Если chat_id или media не указаны.
        '''
        method = 'sendMediaGroup'
        files = {}
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif media is None or not isinstance(media, list) or len(media) == 0:
            raise ValueError("media должен быть непустым списком")
        elif len(media) > 10:
            raise ValueError("Нельзя отправлять более 10 объектов в одном сообщении (ограничение Telegram)")
        media_payload = []
        for i, item in enumerate(media):
            if isinstance(item, (InputMediaPhoto, InputMediaAnimation, InputMediaVideo, InputMediaAudio, InputMediaDocument)):
                media_payload.append(item.to_dict())
            elif isinstance(item, str):
                media_payload.append({'type': 'photo', 'media': item})
            elif isinstance(item, bytes):
                file_key = f"media{i}"
                media_payload.append({'type': 'photo', 'media': f'attach://{file_key}'})
                files[file_key] = item
            else:
                raise ValueError("Элемент media должен быть экземпляром str, bytes или одного из классов InputMedia.")
        params = {
            'chat_id': chat_id,
            'media': json.dumps(media_payload),
            'disable_notification': disable_notification}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params, files=files if files else None)
        if response and 'result' in response:
            return [Message.from_dict(item) for item in response['result']]
        return None

    def edit_message_reply_markup(self, chat_id: Union[int, str] = None, message_id: int = None, reply_markup: Union[dict, Markup] = None, inline_message_id: str = None) -> bool:
        '''Редактирует клавиатуру сообщения'''
        method = 'editMessageReplyMarkup'
        if chat_id is None:
            raise ValueError("chat_id не должен быть None")
        elif message_id is None:
            raise ValueError("message_id не должен быть None")
        elif reply_markup is None:
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
    
    def edit_message_live_location(self, chat_id: Union[int, str] = None, message_id: int = None,
                                   inline_message_id: str = None, latitude: float = None, longitude: float = None,
                                   horizontal_accuracy: float = None, heading: int = None,
                                   proximity_alert_radius: int = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''Редактирует живую локацию сообщения'''
        method = 'editMessageLiveLocation'
        if (chat_id is None and inline_message_id is None) or latitude is None or longitude is None:
            raise ValueError("Необходимы либо chat_id и message_id, либо inline_message_id, а также latitude и longitude")
        params = {
            'chat_id': chat_id,
            'message_id': message_id,
            'inline_message_id': inline_message_id,
            'latitude': latitude,
            'longitude': longitude,
            'horizontal_accuracy': horizontal_accuracy,
            'heading': heading,
            'proximity_alert_radius': proximity_alert_radius,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        return None

    def stop_message_live_location(self, chat_id: Union[int, str] = None, message_id: int = None,
                                   inline_message_id: str = None, reply_markup: Union[dict, Markup] = None) -> Optional['Message']:
        '''Останавливает обновление живой локации сообщения'''
        method = 'stopMessageLiveLocation'
        if chat_id is None and inline_message_id is None:
            raise ValueError("Необходимы либо chat_id и message_id, либо inline_message_id")
        params = {
            'chat_id': chat_id,
            'message_id': message_id,
            'inline_message_id': inline_message_id,
            'reply_markup': json.dumps(reply_markup) if reply_markup is not None else None}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Message.from_dict(response['result'])
        return None

#Вэбхук    
    def set_webhook(self, url: str = None, certificate: str = None, max_connections: int = None, allowed_updates: list | str = None) -> Optional['WebhookInfo']:
        '''Устанавливает вебхук'''
        method = 'setWebhook'
        if url is None:
            raise ValueError("url не может быть None")
        elif max_connections is None:
            raise ValueError("max_connections не может быть None")
        elif allowed_updates is None:
            raise ValueError("allowed_updates не может быть None")
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
    def get_updates(self, timeout: int = 45, allowed_updates: Union[list, str] = None, long_polling_timeout: int = 45) -> list:
        '''Запрос обновлений с учетом дополнительных параметров'''
        method = 'getUpdates'
        params = {'timeout': timeout, 'allowed_updates': allowed_updates, 'offset': self.update_offset, 'long_polling_timeout': long_polling_timeout}
        params = {k: v for k, v in params.items() if v is not None}
        updates = self._make_request(method, params)
        if updates and 'result' in updates:
            return updates['result']
        return []

    def process_updates(self, updates: list = None):
        '''Обрабатывает полученные обновления'''
        if updates is None:
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

    def always_polling(self, interval: int = 1, timeout: int = 45, long_polling_timeout: int = 45, allowed_updates: Union[list, str] = None, restart_on_error: bool = True):
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
    def get_chat(self, chat_id: Union[int, str] = None) -> Optional['Chat']:
        '''Получает информацию о чате'''
        method = 'getChat'
        if chat_id is None:
            raise ValueError("chat_id не может быть None")
        params = {'chat_id': chat_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return Chat.from_dict(response['result'])
        else:
            return None

    def get_chat_administrators(self, chat_id: Union[int, str] = None) -> Union['ChatMember', list]:
        '''Получает список администраторов чата'''
        method = 'getChatAdministrators'
        if chat_id is None:
            raise ValueError("chat_id не может быть None")
        params = {'chat_id': chat_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return [ChatMember.from_dict(admin) for admin in response['result']]
        else:
            return []

    def get_chat_members_count(self, chat_id: Union[int, str] = None) -> int:
        '''Получает количество участников чата'''
        method = 'getChatMemberCount'
        if chat_id is None:
            raise ValueError("chat_id не может быть None")
        params = {'chat_id': chat_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return response['result']
        else:
            return 0

    def get_chat_member(self, chat_id: Union[int, str] = None, user_id: int = None) -> Optional['ChatMember']:
        '''Получает информацию о пользователе чата и его статус'''
        method = 'getChatMember'
        if chat_id is None:
            raise ValueError("chat_id не может быть None")
        elif user_id is None:
            raise ValueError("user_id не может быть None")
        params = {'chat_id': chat_id, 'user_id': user_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return ChatMember.from_dict(response['result'])
        else:
            return None

    def set_chat_photo(self, chat_id: Union[int, str] = None, photo: Union[str, bytes, InputFile] = None) -> bool:
        '''Устанавливает фото для чата'''
        method = 'setChatPhoto'
        if chat_id is None:
            raise ValueError("chat_id не может быть None")
        elif photo is None:
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

    def delete_chat_photo(self, chat_id: Union[int, str] = None) -> bool:
        '''Удаляет фотографию чата'''
        method = 'deleteChatPhoto'
        if chat_id is None:
            raise ValueError("chat_id не может быть None")
        params = {'chat_id': chat_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def set_chat_title(self, chat_id: Union[int, str] = None, title: str = None) -> bool:
        '''Устанавливает название чата'''
        method = 'setChatTitle'
        if chat_id is None:
            raise ValueError("chat_id не может быть None")
        elif title is None:
            raise ValueError("title не может быть None")
        elif len(title) < 1 or len(title) > 128:
            raise ValueError("Название чата должно быть от 1 до 128 символов")
        params = {'chat_id': chat_id, 'title': title}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def set_chat_description(self, chat_id: Union[int, str] = None, description: str = None) -> bool:
        '''Устанавливает описание для чата'''
        method = 'setChatDescription'
        if chat_id is None:
            raise ValueError("chat_id не может быть None")
        elif description is None:
            raise ValueError("description не может быть None")
        elif len(description) < 0 or len(description) > 255:
            raise ValueError("Описание чата должно быть от 0 до 255 символов")
        params = {'chat_id': chat_id, 'description': description}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def leave_chat(self, chat_id: Union[int, str] = None) -> bool:
        '''Покидает чат'''
        method = 'leaveChat'
        if chat_id is None:
            raise ValueError("chat_id не может быть None")
        params = {'chat_id': chat_id}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False
    
# Административные команды
    def kick_chat_member(self, chat_id: Union[int, str] = None, user_id: int = None, until_date: float = None) -> bool:
        '''Выгоняет пользователя из чата'''
        method = 'kickChatMember'
        if chat_id is None:
            raise ValueError("chat_id не может быть None")
        elif user_id is None:
            raise ValueError("user_id не может быть None")
        elif until_date is None:
            until_date = time.time()
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

    def ban_chat_member(self, chat_id: Union[int, str] = None, user_id: int = None, until_date: float = None, revoke_messages: bool = False) -> bool:
        '''Блокирует пользователя в чате'''
        method = 'banChatMember'
        if chat_id is None:
            raise ValueError("chat_id не может быть None")
        elif user_id is None:
            raise ValueError("user_id не может быть None")
        elif until_date is None:
            until_date = time.time()
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

    def unban_chat_member(self, chat_id: Union[int, str] = None, user_id: int = None, only_if_banned: bool = False) -> bool:
        '''Разблокирует пользователя в чате'''
        method = 'unbanChatMember'
        if chat_id is None:
            raise ValueError("chat_id не может быть None")
        elif user_id is None:
            raise ValueError("user_id не может быть None")
        params = {'chat_id': chat_id, 'user_id': user_id, 'only_if_banned': only_if_banned}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def mute_user(self, chat_id: Union[int, str] = None, user_id: int = None, duration: int = 3600) -> bool:
        '''Заблокирует отправку сообщений для пользователя в чате'''
        method = 'restrictChatMember'
        if chat_id is None:
            raise ValueError("chat_id не может быть None")
        elif user_id is None:
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

    def unmute_user(self, chat_id: Union[int, str] = None, user_id: int = None) -> bool:
        '''Разблокирует отправку сообщений для пользователя в чате'''
        method = 'restrictChatMember'
        if chat_id is None:
            raise ValueError("chat_id не может быть None")
        elif user_id is None:
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

    def restrict_chat_member(self, chat_id: Union[int, str] = None, user_id: int = None, permissions: ChatPermissions = None, until_date: float = None) -> bool:
        '''Изменяет разрешения пользователя в чате'''
        method = 'restrictChatMember'
        if chat_id is None:
            raise ValueError("chat_id не может быть None")
        elif user_id is None:
            raise ValueError("user_id не может быть None")
        elif permissions is None:
            raise ValueError("permissions не может быть None")
        elif until_date is None:
            until_date = time.time()
        params = {
            'chat_id': chat_id,
            'user_id': user_id,
            'permissions': permissions.to_dict(),
            'until_date': until_date}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

    def promote_chat_member(self, chat_id: Union[int, str] = None, user_id: int = None, can_change_info: bool = False, can_post_messages: bool = False, can_edit_messages: bool = False, can_delete_messages: bool = False, can_invite_users: bool = False, can_restrict_members: bool = False, can_pin_messages: bool = False, can_promote_members: bool = False) -> bool:
        '''Изменяет права пользователя в чате'''
        method = 'promoteChatMember'
        if chat_id is None:
            raise ValueError("chat_id не может быть None")
        elif user_id is None:
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

    def set_chat_permissions(self, chat_id: Union[int, str] = None, permissions: ChatPermissions = None) -> bool:
        '''Устанавливает права для всех участников чата'''
        method = 'setChatPermissions'
        if chat_id is None:
            raise ValueError("chat_id не может быть None")
        elif permissions is None:
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
        '''
        Декоратор для регистрации обработчика сообщений.

        :param func: Функция, которая будет вызвана для фильтрации сообщений.
        :type func: callable, optional
        :param commands: Список команд, на которые реагирует обработчик.
        :type commands: list[str], optional
        :param regexp: Регулярное выражение для фильтрации текста сообщений.
        :type regexp: str, optional
        :param content_types: Типы контента, на которые реагирует обработчик.
        :type content_types: list[str], optional
        :return: Декоратор для обработчика.
        :rtype: callable
        '''
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

    def _handle_message(self, message_data: dict = None) -> None:
        '''Обработка сообщений'''
        if message_data is None:
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
            command_full = text.split()[0][1:]
            if '@' in command_full:
                parts = command_full.split('@', 1)
                command = parts[0].lower()
                target_username = parts[1].lower() if len(parts) > 1 else None
            else:
                command = command_full.lower()
                target_username = None
            chat_type = message.chat.type
            if (chat_type == 'private') or (chat_type in ['group', 'supergroup'] and target_username == self.bot_username):
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

    def register_next_step_handler(self, message: Message = None, callback: callable = None, *args: list, **kwargs: dict) -> None:
        '''Регистрирует следующий обработчик для сообщения'''
        if message is None:
            raise ValueError("message не может быть None")
        elif callback is None:
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

    def _handle_callback_query(self, callback_query_data: dict = None) -> None:
        '''Обрабатывает нажатия на инлайн-кнопки'''
        if callback_query_data is None:
            raise ValueError("callback_query_data не может быть None")
        callback_query = CallbackQuery(callback_query_data)
        data = callback_query.data
        for handler in self.handlers['callback_query']:
            if handler['data'] is None or handler['data'] == data:
                if handler['func'] is None or handler['func'](callback_query):
                    handler['function'](callback_query)
                    break

    def answer_callback_query(self, callback_id: str = None, text: str = "Что-то забыли указать", show_alert: bool = False, url: str = None, cache_time: int = 0) -> bool:
        '''Отвечает на запрос callback'''
        method = 'answerCallbackQuery'
        if callback_id is None:
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
    
    def inline_query_handler(self, func: callable = None, query: str = None) -> callable:
        '''Регистрирует inline запросы'''
        def decorator(handler: callable) -> callable:
            self.handlers['inline_query'].append({
                'function': handler,
                'func': func,
                'query': query
            })
            return handler
        return decorator

    def _handle_inline_query(self, inline_query_data: dict = None) -> None:
        '''Обрабатывает inline запросы'''
        if inline_query_data is None:
            raise ValueError("inline_query_data не может быть None")
        inline_query = inline_query_data  
        query_text = inline_query.get('query', '')
        for handler in self.handlers.get('inline_query', []):
            if handler['query'] is None or handler['query'] in query_text:
                if handler['func'] is None or handler['func'](inline_query):
                    handler['function'](inline_query)
                    break

    def answer_inline_query(self, inline_query_id: str = None, results: list = None,
                              cache_time: int = None, is_personal: bool = None, next_offset: str = None,
                              switch_pm_text: str = None, switch_pm_parameter: str = None) -> bool:
        '''Отвечает на inline запрос'''
        method = 'answerInlineQuery'
        if inline_query_id is None:
            raise ValueError("inline_query_id не должен быть None")
        if results is None or not isinstance(results, list):
            raise ValueError("results должен быть непустым списком")
        if results and hasattr(results[0], 'to_dict'):
            results_serialized = json.dumps([result.to_dict() for result in results])
        else:
            results_serialized = json.dumps(results)
        params = {
            'inline_query_id': inline_query_id,
            'results': results_serialized,
            'cache_time': cache_time,
            'is_personal': is_personal,
            'next_offset': next_offset,
            'switch_pm_text': switch_pm_text,
            'switch_pm_parameter': switch_pm_parameter}
        params = {k: v for k, v in params.items() if v is not None}
        response = self._make_request(method, params)
        if response and 'result' in response:
            return True
        else:
            return False

#Фон задача
    def run_in_bg(self, func, *args, **kwargs):
        '''Запускает функцию на фоне'''
        def wrapper():
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f"Error[{func}]: {e}")
        threading.Thread(target=wrapper, daemon=True).start()


#Блок - Нейросети
class FreeGpt:
    def gemini(self, prompt: str = None) -> str:
        '''Генерация текста с помощью Gemini-1.5-pro'''
        try:   
            if prompt is None:
                raise ValueError("Забыли указать prompt")
            data = {"prompt": prompt}
            plik = requests.post(f"https://www.teach-anything.com/api/generate", json=data, timeout=80)
            plik.encoding = "utf-8"
            if plik.status_code == 200:
                return plik.text
            else:
                return "Error"
        except Exception as e:
            print(f"FreeAI(gemini): {e}")
            return "Error"

    def searchX(self, query: str = None, count: int = 10) -> dict:
        '''Поиск информации с помощью https://www.chatwithmono.xyz\ncount: кол-во результатов'''
        try:
            if query is None:
                raise ValueError("Забыли указать query")
            payload = {"query": query, "count": count}
            resp = requests.post("https://www.chatwithmono.xyz/api/search", json=payload)
            if resp.status_code == 200:
                data = resp.json()
                site_titles = [result["title"] for result in data["results"]]
                site_urls = [result["url"] for result in data["results"]]
                result_list = []
                for i in range(len(site_titles)):
                    result_list.append(site_titles[i])
                    result_list.append(site_urls[i])
                return result_list
            else:
                return False
        except Exception as e:
            print(f"FreeAI(searchX): {e}")
            return False

    def toolchat(self, prompt: str = None, model_index: int = 0) -> str:
        '''Генерация ответа используя Toolbaz\nДоступные модели: 0 - Gemini-2.5-flash; 1 - Gemini-2.0-flash-thinking; 2 - Gemini-2.0-flash; 3 - Gemini-1.5-flash"; 4 -  o3-mini; 5 - Gpt-4o-latest; 6 - Gpt-4o; 7 - Grok-3-beta; 8 - Grok-2-1212; 9 - Sonar; 10 - Llama-4-Maverick; 11 - Llama-4-Scout; 12 - Llama-3.3-70B; 13 - Deepseek-R1, 14 - Toolbaz_v3.5_pro; 15 - Toolbaz_v3; 16 - Mixtral_8x22b; 17 - L3-70B-Euryale-v2.2; 18 - Midnight-rose; 19 - Unity; 20 - Unfiltered_x'''
        try:
            HEADERS = {
                "accept": "*/*",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "origin": "https://toolbaz.com",
                "referer": "https://toolbaz.com/",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"}
            MODELS = ["gemini-2.5-flash", "gemini-2.0-flash-thinking", "gemini-2.0-flash", "gemini-1.5-flash", "o3-mini", "gpt-4o-latest", "gpt-4o", "grok-3-beta", "grok-2-1212", "sonar", "Llama-4-Maverick", "Llama-4-Scout", "Llama-3.3-70B", "deepseek-r1", "toolbaz_v3.5_pro", "toolbaz_v3", "mixtral_8x22b", "L3-70B-Euryale-v2.1", "midnight-rose", "unity", "unfiltered_x"]
            if prompt is None:
                raise ValueError("Забыли указать prompt")
            elif model_index < 0 or model_index >= len(MODELS):
                raise ValueError(f"Неверно указан model_index, минимальное значение 0, максимальное значение {len(MODELS)-1}")
            def random_str(length):
                return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789") for _ in range(length))
            def create_token():
                data = {
                    "bR6wF": {
                        "nV5kP": HEADERS["user-agent"],
                        "lQ9jX": "ru-RU",
                        "sD2zR": "1920x1080",
                        "tY4hL": "Europe/Moscow",
                        "pL8mC": "Win32",
                        "cQ3vD": 24,
                        "hK7jN": 8},
                    "uT4bX": {
                        "mM9wZ": [{"x": random.randint(0, 1920), "y": random.randint(0, 1080)} for _ in range(20)],
                        "kP8jY": [random.choice(string.ascii_letters) for _ in range(10)]},
                    "tuTcS": int(time.time()),
                    "tDfxy": -7,
                    "RtyJt": random_str(36),
                    "extra": {
                        "random_str": random_str(50),
                        "timestamp": str(datetime.datetime.now(datetime.timezone.utc)),
                        "version": "1.0.0"}}
                return random_str(6) + base64.b64encode(json.dumps(data).encode()).decode()
            with requests.Session() as session:
                session.cookies.set("SessionID", "ERfvMHDEY5Fo1TTJu1W7hIZSA9dHcVyJCb5m")
                token_data = {
                    "session_id": "ERfvMHDEY5Fo1TTJu1W7hIZSA9dHcVyJCb5m",
                    "token": create_token()}
                token_response = session.post(f"https://data.toolbaz.com/token.php", data=token_data, headers=HEADERS)
                if not token_response.json().get("token"):
                    return None
                payload = {
                    "text": prompt,
                    "capcha": token_response.json()["token"],
                    "model": MODELS[model_index],
                    "session_id": "ERfvMHDEY5Fo1TTJu1W7hIZSA9dHcVyJCb5m"}
                response = session.post(f"https://data.toolbaz.com/writing.php", data=payload, headers=HEADERS)
                if response.status_code == 200:
                    return response.text
                else:
                    return "Error"
        except Exception as e:
            print(f"FreeAI(toolchat): {e}")
            return "Error"

    def deepchat(self, messages: dict = None, model: str = "Qwen/Qwen3-235B-A22B", temperature: float = 0.7, max_tokens: int = None, timeout: int = 80) -> str:
        '''Генерация ответа используя DeepInfra\nДоступне модели смотреть тут: https://deepinfra.com/models'''
        try:
            if messages is None:
                raise ValueError("Забыли указать messages")
            payload = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
            response = requests.post(
                url="https://api.deepinfra.com/v1/openai/chat/completions",
                json=payload,
                timeout=timeout)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return "Error"
        except Exception as e:
            print(f"FreeAI(deepchat): {e}")
            return "Error"
    
    def mono_chat(self, messages: dict = None, model: str = "o4-mini") -> str:
        '''Генерация ответа с использованием https://www.chatwithmono.xyz'''
        try:
            if messages is None:
                raise ValueError("Забыли указать messages")
            payload = {"messages": messages, "model": model}
            full_response = ""
            with requests.post("https://www.chatwithmono.xyz/api/chat", json=payload, stream=True, timeout=(30, 360)) as res:
                res.raise_for_status()
                for chunk in res.iter_lines(decode_unicode=True):
                    if not chunk:
                        continue
                    line = chunk.strip()
                    if line.startswith('0:"') and line.endswith('"'):
                        try:
                            text_piece = json.loads(line[2:])
                            full_response += text_piece
                        except json.JSONDecodeError:
                            continue
            return full_response.strip()
        except Exception as e:
            print(f"FreeAI(mono_chat): {e}")
            return "Error"
    
    def poll_ai(self, messages: dict = None, model: str = "searchgpt", temperature: float = 0.7) -> str:
        '''Генерация ответа с использованием https://pollinations.ai/'''
        try:
            if messages is None:
                raise ValueError("Забыли указать messages")
            payload = {"messages": messages, "model": model, "temperature": temperature, "stream": False, "private": True, "seed": random.randint(0, 1000)}
            resp = requests.post("https://text.pollinations.ai/openai", json=payload, headers={'Content-Type': 'application/json'})
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
            else:
                return "Error"
        except Exception as e:
            print(f"FreeAI(poll_ai): {e}")
            return "Error"

    def speech(self, text: str = None, voice: str = "nova", filename: str = "ozv") -> bool:
        '''Озвучивание текста'''
        try:
            if text is None:
                raise ValueError("`text` must be provided and non-empty.")
            if len(text) > 4096:
                raise ValueError("`text` length must not exceed 4096 characters.")
            if voice not in ["alloy", "ash", "ballad", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer", "verse"]:
                raise ValueError(f"Unsupported voice: {voice}. Supported: alloy, ash, ballad, coral, echo, fable, onyx, nova, sage, shimmer, verse")
            payload = {"input": text, "prompt": f"Voice: {voice}. Standard clear voice.", "voice": voice, "vibe": "null"}
            response = requests.post(
                url="https://www.openai.fm/api/generate",
                headers={
                    "accept": "*/*", "accept-encoding": "gzip, deflate, br, zstd",
                    "accept-language": "en-US,en;q=0.9,hi;q=0.8", "dnt": "1",
                    "origin": "https://www.openai.fm", "referer": "https://www.openai.fm/",
                    "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")},
                data=payload,
                timeout=80)
            if response.status_code == 200:
                with open(f"{filename}.mp3", "wb") as f:
                    f.write(response.content)
                return True
            else:
                return False
        except Exception as e:
            print(f"FreeAI(speech): {e}")
            return False
    
    def encode_base64(self, path: str = None) -> str:
        '''Кодирование в base64'''
        try:
            if path is None:
                raise ValueError("`path` must be provided and non-empty.")
            with open(path, "rb") as file:
                return base64.b64encode(file.read()).decode('utf-8')
        except FileNotFoundError:
            return None


class FreeImg:
    def art(self, prompt: str, ind: int = 2, steps: int = 50, negative: str = "painting, extra fingers, mutated hands, poorly drawn hands, deformed, ugly", filename: str = "image.png") -> bool:
        '''Генерация фотографии с помощью Arting.ai/\nModels: 0 - animatedModelsOf_31; 1 - fuwafuwamix_v15BakedVae; 2 - asyncsMIX_v7; 3 - cuteAnime_v10'''
        try:
            models = ["animatedModelsOf_31", "fuwafuwamix_v15BakedVae", "asyncsMIX_v7", "cuteAnime_v10"]
            if prompt is None:
                raise ValueError("Забыли указать prompt")
            elif ind < 0 or ind >= len(models):
                raise ValueError("Неверный индекс модели")
            payload = {
                "prompt": prompt,
                "model_id": models[ind],
                "samples": 1,
                "height": "1024",
                "width": "1024",
                "negative_prompt": negative,
                "seed": -1,
                "lora_ids": "",
                "lora_weight": "0.7",
                "sampler": "DPM2",
                "steps": steps,
                "guidance": 7,
                "clip_skip": 2}
            with requests.Session() as session:
                create = session.post("https://api.arting.ai/api/cg/text-to-image/create", json=payload, timeout=30)
                create.raise_for_status()
                request_id = create.json().get("data", {}).get("request_id")
                for _ in range(10):
                    time.sleep(3)
                    get = session.post("https://api.arting.ai/api/cg/text-to-image/get", json={"request_id": request_id}, timeout=30)
                    get.raise_for_status()
                    data = get.json()
                    if data["code"] == 100000 and data["data"]["output"]:
                        url = data["data"]["output"][0]
                        r = session.get(url, timeout=30)
                        if r.status_code in [200, 201]:
                            with open(filename, "wb") as f:
                                f.write(r.content)
                            return True
                        else:
                            return False
                else:
                    return False
        except Exception as e:
            print(f"FreeImg(art): {e}")
            return False

    def mono_img(self, prompt: str = None, model: int = 0, filename: str = "image.png") -> bool:
        '''Генерация фотографии с помощью https://www.chatwithmono.xyz\nModels: 0 - nextlm-image-1; 1 - gpt-image-1; 2 - dall-e-3; 3 - dall-e-2'''
        try:
            if prompt is None:
                raise ValueError("Забыли указать prompt")
            MoD = ["nextlm-image-1", "gpt-image-1", "dall-e-3", "dall-e-2"]
            payload = {"prompt": prompt, "model": MoD[model]}
            resp = requests.post("https://www.chatwithmono.xyz/api/image", json=payload, timeout=(30, 360))
            if resp.status_code == 200:
                data = resp.json()
                image_base64 = data.get("image")
                with open(filename, "wb") as f:
                    f.write(base64.b64decode(image_base64))
                return True
            else:
                return False
        except Exception as e:
            print("FreeImg(mono_img):", e)
            return False
    
    def poll_img(self, prompt: str = None, width: int = 1024, height: int = 1024, enhance: bool = True, private: bool = True, nologo: bool = True, model: str = 'flux', filename: str = 'image.png') -> bool:
        '''Генерация фотографии с помощью моделей pollinations.ai\nModels: flux, turbo, gptimage'''
        try:
            if prompt is None:
                raise ValueError("Забыли указать prompt")
            prompt = prompt.replace(" ", "%20")
            seed = random.randint(0, 1000)
            response = requests.get(f"https://pollinations.ai/prompt/{prompt}?width={width}&height={height}&seed={seed}&enhance={enhance}&private={private}&nologo={nologo}&model={model}", timeout=80)
            if response.status_code == 200:
                with open(filename, 'wb') as file:
                    file.write(response.content)
                return True
            else:
                return False
        except Exception as e:
            print(f"FreeAI(poll_img): {e}")
            return False
    
    def flux(self, prompt: str = None, filename: str = 'image.png') -> bool:
        '''Генерация фотографии с помощью Flux'''
        try:
            if prompt is None:
                raise ValueError("Забыли указать prompt")
            prompt = prompt.replace(" ", "%20")
            resp = requests.get('https://lusion.regem.in/access/flux-2.php', params={'prompt': prompt}, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', 'referer': 'https://lusion.regem.in/'})
            if resp.status_code == 200:
                if resp.text == "Error! Try Again Later":
                    return False
                soup = bs4.BeautifulSoup(resp.text, 'html.parser')
                img = soup.find('img', class_='img-fluid rounded')
                src = img['src']
                base64_string = src.split(',')[1]
                img_bytes = base64.b64decode(base64_string)
                with open(filename, 'wb') as file:
                    file.write(img_bytes)
                return True
            else:
                return False
        except Exception as e:
            print(f"FreeAI(flux): {e}")
            return False


class Translate:
    def __init__(self):
        self.headers = {"accept": "application/json, text/plain, */*", 
		"api-key": "pDwCjq7CyeAmn1Z3osNunACg2U0SLIhwBTtsp1WqYFMf5UuSIvMBYGS4pt8OIsGMH", 
		"cache-control": "no-cache", 
		"connection": "keep-alive", 
		"content-type": "application/json", 
		"origin": "https://www.aitranslator.com", 
		"referer": "https://www.aitranslator.com/", 
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36", 
		"domain": 'https://aitranslator.com'}
    
    def google(self, text: str = None, target: str = None, source='auto') -> str:
        '''Перевод с помощью Google'''
        try:
            if text is None:
                raise ValueError("Забыли указать text")
            elif target is None:
                raise ValueError("Забыли указать target")
            resp = requests.post('https://api.aitranslator.com/v1/translation/google', headers=self.headers, json={"text": text, "source_language_code": self.detect(text), "target_language_code": target, "share_id": self._shareId()['share_id']})
            resp.raise_for_status()
            return resp.json()['response']['translated_text']
        except Exception as e:
            print(f"Translate(google): {e}")
            return False
    
    def deepl(self, text: str = None, target: str = None, source='auto') -> str:
        '''Перевод с помощью DeepL'''
        try:
            if text is None:
                raise ValueError("Забыли указать text")
            elif target is None:
                raise ValueError("Забыли указать target")
            resp = requests.post('https://api.aitranslator.com/v1/translation/deepl', headers=self.headers, json={"text": text, "source_language_code": self.detect(text), "target_language_code": target, "share_id": self._shareId()['share_id']})
            resp.raise_for_status()
            return resp.json()['response']['translated_text']
        except Exception as e:
            print(f"Translate(deepl): {e}")
            return False
    
    def chat_gpt(self, text: str = None, target: str = None, source='auto') -> str:
        '''Перевод с помощью ChatGPT'''
        try:
            if text is None:
                raise ValueError("Забыли указать text")
            elif target is None:
                raise ValueError("Забыли указать target")
            resp = requests.post('https://api.aitranslator.com/v1/translation/chat-gpt', headers=self.headers, json={"text": text, "source_language_code": self.detect(text), "target_language_code": target, "share_id": self._shareId()['share_id']})
            resp.raise_for_status()
            return resp.json()['response']['translated_text']
        except Exception as e:
            print(f"Translate(chat_gpt): {e}")
            return False
    
    def claude(self, text: str = None, target: str = None, source='auto') -> str:
        '''Перевод с помощью Claude'''
        try:
            if text is None:
                raise ValueError("Забыли указать text")
            elif target is None:
                raise ValueError("Забыли указать target")
            resp = requests.post('https://api.aitranslator.com/v1/translation/claude', headers=self.headers, json={"text": text, "source_language_code": self.detect(text), "target_language_code": target, "share_id": self._shareId()['share_id']})
            resp.raise_for_status()
            return resp.json()['response']['translated_text']
        except Exception as e:
            print(f"Translate(claude): {e}")
            return False

    def lingvanex(self, text: str = None, target: str = None, source='auto') -> str:
        '''Перевод с помощью Lingvanex'''
        try:
            if text is None:
                raise ValueError("Забыли указать text")
            elif target is None:
                raise ValueError("Забыли указать target")
            resp = requests.post('https://api.aitranslator.com/v1/translation/lingvanex', headers=self.headers, json={"text": text, "source_language_code": self.detect(text), "target_language_code": target, "share_id": self._shareId()['share_id']})
            resp.raise_for_status()
            return resp.json()['response']['translated_text']
        except Exception as e:
            print(f"Translate(lingvanex): {e}")
            return False
    
    def detect(self, text: str = None) -> str:
        '''Определение языка'''
        try:
            if text is None:
                raise ValueError("Забыли указать text")
            resp = requests.post('https://api.aitranslator.com/v1/detect/language', headers=self.headers, json={"text": text[:100]})
            resp.raise_for_status()
            return resp.json()['data']['language_probability']['code']
        except Exception as e:
            print(f"Translate(detect): {e}")
            return False
    
    def _shareId(self):
        '''Получение share_id'''
        try:
            resp = requests.post('https://api.aitranslator.com/v1/translation/share-id', headers=self.headers, json={"total_words": None})
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"Translate(_shareId): {e}")
            return False


class ChatGPT:
    def __init__(self, url: str, headers: dict):
        self.url = url.rstrip("/")
        self.headers = headers

    def _make_request(self, method: str, endpoint: str, data: dict = None, files: dict = None) -> Union[dict, list]:
        try:
            url = f"{self.url}/{endpoint.lstrip('/')}"
            if files:
                response = requests.request(method=method, url=url, headers=self.headers, files=files, data=data)
            else:
                response = requests.request(method=method, url=url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"ChatGPT({endpoint}): {e}")
            return "Error"

    def generate_chat_completion(self, model: str, messages: list, temperature: float = None, max_tokens: int = None, stream: bool = False, **kwargs) -> Union[dict, list]:
        data = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens, "stream": stream, **kwargs}
        return self._make_request("POST", "chat/completions", data=data)

    def generate_image(self, prompt: str, n: int = 1, size: str = "1024x1024", response_format: str = "url", **kwargs) -> dict:
        data = {"prompt": prompt, "n": n, "size": size, "response_format": response_format, **kwargs}
        return self._make_request("POST", "images/generations", data=data)

    def generate_embedding(self, model: str, input_i: Union[str, list], user: str = None, **kwargs) -> dict:
        data = {"model": model, "input": input_i, "user": user, **kwargs}
        return self._make_request("POST", "embeddings", data=data)

    def generate_transcription(self, file: BinaryIO, model: str, language: str = None, prompt: str = None, response_format: str = "json", temperature: float = 0, **kwargs) -> Union[dict, str]:
        data = {"model": model, "language": language, "prompt": prompt, "response_format": response_format, "temperature": temperature, **kwargs}
        files = {"file": file}
        return self._make_request("POST", "audio/transcriptions", data=data, files=files)

    def generate_translation(self, file: BinaryIO, model: str, prompt: str = None, response_format: str = "json", temperature: float = 0, **kwargs) -> Union[dict, str]:
        data = {"model": model, "prompt": prompt, "response_format": response_format, "temperature": temperature, **kwargs}
        files = {"file": file}
        return self._make_request("POST", "audio/translations", data=data, files=files)
    
    def get_models(self):
        return self._make_request("GET", "models")