from dotenv import load_dotenv

from src.channel import Channel

load_dotenv()


class Video:
    """Класс для видео"""

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Данные будут подтягиваться по API при первом запросе."""
        self.__video_id = video_id
        self.title = None
        self.video_url = None
        self.view_count = None
        self.like_count = None
        self.update_info()

    def update_info(self):
        request = Channel.get_service().videos().list(
            part="snippet,statistics",
            id=self.__video_id
        )
        response = request.execute()

        video_info = response.get('items', [])
        if video_info:
            video_info = video_info[0]
            snippet = video_info.get('snippet', {})
            statistics = video_info.get('statistics', {})

            self.title = snippet.get('title', 'N/A')
            self.video_url = f"https://www.youtube.com/watch?v={self.__video_id}"
            self.view_count = int(statistics.get('viewCount', 0))
            self.like_count = int(statistics.get('likeCount', 0))

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):
    """Класс для видео с информацией о плейлисте"""

    def __init__(self, video_id: str, playlist_id: str) -> None:
        """Экземпляр инициализируется id видео и id плейлиста."""
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_title = None
        self.update_playlist_info()

    def update_playlist_info(self):
        request = Channel.get_service().playlists().list(
            part="snippet",
            id=self.playlist_id
        )
        response = request.execute()

        playlist_info = response.get('items', [])
        if playlist_info:
            playlist_info = playlist_info[0]
            snippet = playlist_info.get('snippet', {})
            self.playlist_title = snippet.get('title', 'N/A')

    def __str__(self):
        return f"{self.title} ({self.video_url}, Playlist: {self.playlist_title})"
