import os
import json
import subprocess
import random
from pathlib import Path

class filesManager():
    def __init__(self):
        #Busco y creo la carpeta de la musica si esta no existe
        self.base_dir = Path(__file__).resolve().parent.parent
        self.music_dir = self.base_dir / 'Music'
        self.icons_dir = self.base_dir / 'icons'
        self.config = self.base_dir / 'config.json'

        if not os.path.isdir(self.music_dir):
            os.mkdir(self.music_dir)

        self.current_directory = self.load_config()
        self.songs = []
        self.copy_songs = []
        self.current_index = -1       

        self.load_playlist() 

    def load_config(self):
        #Si existe el json lo abro
        if self.config.is_file():
            try:
                with open(self.config,'r') as f:
                    active_dir = json.load(f)
                    if os.path.isdir(active_dir):
                        return active_dir
            except Exception:
                pass
        
        #Si no existe, lo creo
        with open(self.config,'w') as f:
            json.dump(str(self.music_dir),f)
            return self.music_dir

    def save_config(self,new_drt):
        self.current_directory = new_drt
        #SI no existe el json lo creo    
        with open(self.config,'w') as f:
            json.dump(new_drt, f)    
        
    def load_playlist(self):
        self.songs.clear()
        formats = ".mp3"
        if os.path.isdir(self.current_directory):
            for file in os.listdir(self.current_directory):
                if file.lower().endswith(formats):
                    self.songs.append(file)

    def open_folder(self,value=None):
        try:   
            return os.startfile(self.current_directory)
        except:
            return subprocess.Popen(['xdg-open',self.current_directory])

    def set_folder(self, new_drt):
        if os.path.isdir(new_drt):
            self.current_directory = new_drt 
            self.save_config(new_drt)
            self.copy_songs = []
            self.load_playlist()
            return True
        return False

    def next_song(self):
        if not self.songs:
            return None

        self.current_index += 1
        if self.current_index >= len(self.songs):
            self.current_index = 0
        
        return self.songs[self.current_index]
            
    def prev_song(self):
        if not self.songs:
            return None
        
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = len(self.songs) - 1

        return self.songs[self.current_index]

    def get_song_path(self,song_name):
        return os.path.join(self.current_directory, song_name)

    def set_song_index(self,song_name):
        if song_name in self.songs:
            self.current_index = self.songs.index(song_name)

    def shuffle_song(self,state,song_name):
        if not state:
            self.copy_songs = self.songs.copy()
            random.shuffle(self.songs)

            if song_name in self.songs:
                swap = self.songs.index(song_name)
                
                self.songs[0],self.songs[swap] = self.songs[swap], self.songs[0]
                self.current_index = 0
        else:
            if self.copy_songs :
                self.songs = self.copy_songs.copy()
            if song_name in self.songs:
                self.current_index = self.songs.index(song_name)
            else:
                self.current_index = -1
            return self.songs