import os
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

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        request = self.youtube.channels().list(
            part="snippet,statistics",
            id=self.channel_id
        )
        response = request.execute()

        channel_info = response.get('items', [])[0]
        if channel_info:
            snippet = channel_info.get('snippet', {})
            statistics = channel_info.get('statistics', {})

            print(f"Channel ID: {self.channel_id}")
            print(f"Title: {snippet.get('title', 'N/A')}")
            print(f"Description: {snippet.get('description', 'N/A')}")
            print(f"Subscribers: {statistics.get('subscriberCount', 'N/A')}")
            print(f"View Count: {statistics.get('viewCount', 'N/A')}")
        else:
            print("Unable to fetch channel information.")
