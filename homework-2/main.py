from src.channel import Channel

if __name__ == '__main__':
    moscowpython = Channel('UC-OVMPlMA3-YCIeg4z5z23A')

    print("Channel ID:", moscowpython.channel_id)
    print("Title:", moscowpython.title)
    print("Description:", moscowpython.description)
    print("Link:", moscowpython.link)
    print("Subscribers:", moscowpython.subscribers)
    print("Videos:", moscowpython.videos)
    print("Views:", moscowpython.views)

    moscowpython.to_json('moscowpython.json')
