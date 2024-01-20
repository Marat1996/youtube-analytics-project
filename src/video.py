from datetime import timedelta

from src.channel import Channel



class Video:
    def __init__(self, video_id, title=None, video_url=None, view_count=None, like_count=None, duration=None):
        self.__video_id = video_id
        self.title = title
        self.video_url = video_url
        self.view_count = view_count
        self.like_count = like_count
        self.duration = duration
        self.url = f"https://www.youtube.com/watch?v={video_id}"  # Добавьте эту строку

        try:
            if not all((title, video_url, view_count, like_count, duration)):
                self.update_info()
        except Exception as e:
            # Обработка исключения при ошибке запроса данных по API
            print(f"Error updating video info: {e}")
            self.title = None
            self.video_url = None
            self.view_count = None
            self.like_count = None
            self.duration = None

    def update_info(self):
        request = Channel.get_service().videos().list(
            part="snippet,statistics,contentDetails",
            id=self.__video_id
        )
        response = request.execute()

        video_info = response.get('items', [])
        if video_info:
            video_info = video_info[0]
            snippet = video_info.get('snippet', {})
            statistics = video_info.get('statistics', {})
            content_details = video_info.get('contentDetails', {})

            self.title = snippet.get('title')
            self.video_url = f"https://www.youtube.com/watch?v={self.__video_id}"
            self.view_count = statistics.get('viewCount')

            # Обработка случая, когда информация о лайках отсутствует
            self.like_count = statistics.get('likeCount', 0)

            duration_iso = content_details.get('duration', 'PT0S')
            self.duration = self._parse_duration(duration_iso)

    def _parse_duration(self, duration_iso):
        time_elements = duration_iso.split('T')[1].split(':')
        hours, minutes, seconds = 0, 0, 0

        for element in time_elements:
            if 'H' in element:
                hours = int(element[:-1])
            elif 'M' in element:
                if 'S' in element:
                    minutes, seconds = map(int, element[:-1].split('M'))
                else:
                    minutes = int(element[:-1])
            elif 'S' in element:
                seconds = int(element[:-1])

        return timedelta(hours=hours, minutes=minutes, seconds=seconds)
