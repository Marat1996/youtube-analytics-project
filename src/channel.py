import json
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Данные будут подтягиваться по API при первом запросе."""
        self._title = None
        self.__channel_id = channel_id
        self.api_key = os.getenv('YOU_TUBE_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    @property
    def title(self):
        if self._title is None:
            self.update_info()
        return self._title

    @property
    def channel_id(self):
        return self.__channel_id

    def update_info(self):
        try:
            request = self.youtube.channels().list(
                part="snippet,statistics",
                id=self.__channel_id
            )
            response = request.execute()

            channel_info = response.get('items', [])[0]
            if channel_info:
                snippet = channel_info.get('snippet', {})
                statistics = channel_info.get('statistics', {})

                self._title = snippet.get('title', 'N/A')
                self.description = snippet.get('description', 'N/A')
                self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
                self.subscribers = int(statistics.get('subscriberCount', 0))
                self.video_count = int(statistics.get('videoCount', 0))
                self.view_count = int(statistics.get('viewCount', 0))
            else:
                print("Unable to fetch channel information.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    @classmethod
    def get_service(cls):
        real_channel_id = "UC-OVMPlMA3-YCIeg4z5z23A"
        return cls(channel_id=real_channel_id)

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