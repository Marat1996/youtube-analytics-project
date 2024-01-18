from src.video import Video, PLVideo

if __name__ == '__main__':
    # Создаем два экземпляра класса
    video1 = Video('AWX4JnAnjBE')  # 'AWX4JnAnjBE' - это id видео из ютуб
    video2 = PLVideo('4fObz_qw9u4', 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC')

    assert 'Moscow Python № 78' in str(video2)
    assert 'GIL в Python: зачем он нужен и как с этим жить' in str(video1)
