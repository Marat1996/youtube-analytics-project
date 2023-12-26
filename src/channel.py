import os
import json
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.api_key = os.getenv('YOU_TUBE_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.title = None
        self.description = None
        self.link = None
        self.subscribers = None
        self.videos = None
        self.views = None
        self.update_info()

    @classmethod
    def get_service(cls):
        return cls(channel_id="YOU_TUBE_API_KEY")

    def to_json(self, filename):
        data = {
            "id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "link": self.link,
            "subscribers": self.subscribers,
            "videos": self.videos,
            "views": self.views
        }

        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=2)

    def update_info(self):
        request = self.youtube.channels().list(
            part="snippet,statistics",
            id=self.channel_id
        )
        response = request.execute()

        channel_info = response.get('items', [])[0]
        if channel_info:
            snippet = channel_info.get('snippet', {})
            statistics = channel_info.get('statistics', {})

            self.title = snippet.get('title', 'N/A')
            self.description = snippet.get('description', 'N/A')
            self.link = f"https://www.youtube.com/channel/{self.channel_id}"
            self.subscribers = int(statistics.get('subscriberCount', 0))
            self.videos = int(statistics.get('videoCount', 0))
            self.views = int(statistics.get('viewCount', 0))
        else:
            print("Unable to fetch channel information.")
