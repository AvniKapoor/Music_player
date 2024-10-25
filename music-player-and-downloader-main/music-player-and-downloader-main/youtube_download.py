import re
import urllib.request
from pytube import YouTube
import os

def download_song(name: str, artist: str, path: str) -> int:
    if not __check_input(name, artist):
        return -1
    current_directory = os.getcwd()
    try:
        os.chdir(path)  # Change the current working directory to the desired path
        url = __find_song(name, artist)
        filename = (artist + '-' + name).replace(' ', '_') + '.m4a'
        download_to = path + '/' + filename
        print(download_to)
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        audio_stream.download(filename=filename)
        return 0  # Successful download
    except Exception as e:
        print(f"Error during download: {e}")
        return -1
    finally:
        os.chdir(current_directory)  # Change back to the original working directory

def __find_song(name: str, artist: str) -> str:
    search_query = name.replace(' ', '+') + '+' + artist.replace(' ', '+')
    search_link = 'https://www.youtube.com/results?search_query=' + search_query
    html = urllib.request.urlopen(search_link)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    url = "https://www.youtube.com/watch?v=" + video_ids[0]
    return url

def __check_input(name: str, artist: str) -> bool:
    if name is None or artist is None:
        return False
    if name.isspace() or artist.isspace() or name == '' or artist == '':
        return False
    allowed_punc = {',', '.', '!', '?', '"'}
    for char1, char2 in zip(name, artist):
        if not char1.isalnum() and not char1.isspace():
            if char1 not in allowed_punc:
                return False
        if not char2.isalnum() and not char2.isspace():
            if char2 not in allowed_punc:
                return False
    return True

if __name__ == "__main__":
    result = download_song("O sajni", "Arjit Singh", "C:/Users/lenovo/Downloads/musicss")
    print("Download Result:", result)
