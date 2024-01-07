import os

from src.channel import Channel

if __name__ == '__main__':
    # Получаем API-ключ из переменной окружения
    api_key = os.getenv('YOU_TUBE_API_KEY')

    # Создаем экземпляр класса Channel с идентификатором канала и API-ключом
    moscowpython = Channel.get_service('UC-OVMPlMA3-YCIeg4z5z23A', api_key)

    # Получаем значения атрибутов
    print(moscowpython.title)  # MoscowPython
    print(moscowpython.video_count)  # 729 (может быть больше)
    print(moscowpython.url)  # https://www.youtube.com/channel/UC-OVMPlMA3-YCIeg4z5z23A

    # Изменяем channel_id и обновляем данные
    moscowpython.update_channel_id('Новое название')
    print(moscowpython.title)  # Обновленное название
    print(moscowpython.url)  # https://www.youtube.com/channel/Новое%20название

    # Создаем файл 'moscowpython.json' с данными по каналу
    moscowpython.to_json('moscowpython.json')