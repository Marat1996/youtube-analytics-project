import json
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()


class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv('YOU_TUBE_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Данные будут подтягиваться по API при первом запросе."""
        self.__channel_id = channel_id
        self.update_info()

    def update_info(self):
        request = self.get_service().channels().list(
            part="snippet,statistics",
            id=self.__channel_id
        )
        response = request.execute()

        channel_info = response.get('items', [])
        if channel_info:
            channel_info = channel_info[0]
            snippet = channel_info.get('snippet', {})
            statistics = channel_info.get('statistics', {})

            self.title = snippet.get('title', 'N/A')
            self.description = snippet.get('description', 'N/A')
            self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
            self.subscribers = int(statistics.get('subscriberCount', 0))
            self.video_count = int(statistics.get('videoCount', 0))
            self.view_count = int(statistics.get('viewCount', 0))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, filename):
        data = {
            "id": self.__channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscribers": self.subscribers,
            "video_count": self.video_count,
            "view_count": self.view_count
        }

        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=2)

    @property
    def channel_id(self):
        return self.__channel_id

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """Метод для сложения каналов."""
        if isinstance(other, Channel):
            return self.subscribers + other.subscribers
        return NotImplemented

    def __sub__(self, other):
        """Метод для вычитания каналов."""
        if isinstance(other, Channel):
            return self.subscribers - other.subscribers
        return NotImplemented

    def __eq__(self, other):
        """Метод для сравнения каналов на равенство."""
        if isinstance(other, Channel):
            return self.subscribers == other.subscribers
        return NotImplemented

    def __lt__(self, other):
        """Метод для сравнения каналов: меньше."""
        if isinstance(other, Channel):
            return self.subscribers < other.subscribers
        return NotImplemented

    def __le__(self, other):
        """Метод для сравнения каналов: меньше или равно."""
        if isinstance(other, Channel):
            return self.subscribers <= other.subscribers
        return NotImplemented

    def __gt__(self, other):
        """Метод для сравнения каналов: больше."""
        if isinstance(other, Channel):
            return self.subscribers > other.subscribers
        return NotImplemented

    def __ge__(self, other):
        """Метод для сравнения каналов: больше или равно."""
        if isinstance(other, Channel):
            return self.subscribers >= other.subscribers
        return NotImplemented


