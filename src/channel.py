import json
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Данные будут подтягиваться по API при первом запросе."""
        self.description = None
        self._title = None
        self.__channel_id = channel_id
        self._api_key = os.getenv('YOU_TUBE_API_KEY')

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
            youtube = self.get_service()
            request = youtube.channels().list(
                part="snippet,statistics",
                id=self.__channel_id
            )
            response = request.execute()

            channel_info = response.get('items', [])
            if channel_info:
                channel_info = channel_info[0]
                snippet = channel_info.get('snippet', {})
                statistics = channel_info.get('statistics', {})

                self._title = snippet.get('title', 'N/A')
                self.description = snippet.get('description', 'N/A')
                self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
                self.subscribers = int(statistics.get('subscriberCount', 0))
                self.video_count = int(statistics.get('videoCount', 0))
                self.view_count = int(statistics.get('viewCount', 0))
            else:
                print(f"Channel information not available for channel_id: {self.__channel_id}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    @classmethod
    def get_service(cls):
        api_key = os.getenv('YOU_TUBE_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

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

    def update_channel_id(self, new_channel_id):
        self.__channel_id = new_channel_id
        self.update_info()
