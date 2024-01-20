from src.channel import Channel
import datetime

from src.video import Video


class PlayList(Channel):
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = None
        self.url = None
        self._videos = None
        self.update_info()

    def update_info(self):
        request = self.get_service().playlists().list(
            part="snippet",
            id=self.playlist_id
        )
        response = request.execute()
        playlist_info = response.get('items', [])
        if playlist_info:
            playlist_info = playlist_info[0]
            snippet = playlist_info.get('snippet', {})
            self.title = snippet.get('title')
            self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        if self._videos is None:
            self._fetch_videos()
        total_duration = sum((video.duration for video in self._videos), datetime.timedelta())

        return total_duration

    def _fetch_videos(self):
        request = self.get_service().playlistItems().list(
            part="contentDetails",
            playlistId=self.playlist_id,
            maxResults=50
        )
        response = request.execute()
        video_ids = [item['contentDetails']['videoId'] for item in response.get('items', [])]
        self._videos = self.get_service().videos().list(part="contentDetails, statistics", id=','.join(video_ids)).execute()
        # self._videos = [Video(video_id) for video_id in video_ids]

    def show_best_video(self):
        best_video = max(self._videos, key=lambda video: video.like_count, default=None)
        return best_video.video_url if best_video and best_video.video_url else None

    def show_best_video(self):
        best_video = max(self._videos, key=lambda video: video.like_count, default=None)
        return best_video.video_url.replace("www.", "") if best_video else None











