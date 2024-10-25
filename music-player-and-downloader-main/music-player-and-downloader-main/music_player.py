from circular_doubly_linked_list import CircularDoublyLinkedList
import pyglet
import os


class Song:
  
    def __init__(self, name: str, artist: str, file: str) -> None:
        self.name = name        # song name
        self.artist = artist    # artist name
        self.file = file        # path to the file

    def get_name(self) -> str:
        return self.name

    def get_artist(self) -> str:
        return self.artist

    def get_file(self) -> str:
        return self.file

    def __eq__(self, other):
       
        return self.get_file() == other.get_file()



class MusicPlayer(CircularDoublyLinkedList):
   
    def __init__(self, playlist_path: str) -> None:
        super().__init__()
        self.playlist_path = playlist_path      # path to playlist folder
        self.player = pyglet.media.Player()     # the sound player
        self.__clean_up(playlist_path)          
        self.__read_files(playlist_path)
        self.now_playing = self.head            # the song that is currently being played
        self.playing = True                     # determine if music is being played or paused
        self.current_song_duration = 0          # the duration of the currently playing song       
        self.__load_current_song()

    
    def to_next_song(self) -> None:
       
        self.now_playing = self.now_playing.next
        self.__load_current_song()

    
    def to_previous_song(self) -> None:
       
        self.now_playing = self.now_playing.prev
        self.__load_current_song()


    def replay(self) -> None:
        
        self.__load_current_song()

    
    def get_song_name(self) -> str:
       
        name = self.now_playing.value.get_name()
        return name
    
    
    def get_artist_name(self) -> str:
       
        artist = self.now_playing.value.get_artist()
        return artist


    def get_song_duration(self) -> float:
       
        return self.current_song_duration

    
    def is_playing(self) -> bool:
       
        return self.playing

    
    def delete_song(self) -> bool:
        
        self.player.pause()
        # remove the song from the folder
        if not os.path.exists(self.now_playing.value.get_file()):
            return False
        os.remove(self.now_playing.value.get_file())
        # remove the song from the linked list (media player)
        if self.remove(self.now_playing.value) == -1:
            return False
        return True

    
    def play_pause(self) -> None:
        
        # if song is playing -> pause it
        if self.playing:
            self.player.pause()
            self.playing = False
        # if is paused -> continue playing
        else:
            self.player.play()
            self.playing = True

    
    def destroy(self) -> None:
        
        self.player.delete()

   
    def __load_current_song(self) -> None:
        
        self.player.next_source()
        src = pyglet.media.load(self.now_playing.value.get_file())
        self.current_song_duration = src.duration
        self.player.queue(src)
        self.player.play()

    
    def __read_files(self, path) -> None:
       
        for file in os .listdir(path):
            string = file.split('-')
            artist = self.__make_readable(string[0])
            name = self.__make_readable(string[1])
            song = Song(name, artist, path + '/' + file)
            self.append(song)

    
    def __clean_up(self, path: str) -> None:
        
        for file in os.listdir(path):
            if not file.endswith('.m4a'):
                os.remove(path + '/' + file)

    
    def __make_readable(self, string: str) -> str:
       
        string = string.removesuffix('.m4a')
        string = string.replace('_', ' ')
        return ''.join((element + ' ') for element in string)
