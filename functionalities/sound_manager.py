import pygame

class soundManager():
    def __init__(self):
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print('Audio initialization failed',e)

        self.playing = False
        self.paused = False
        self.current_file = None
        self.song_length = 0

        self.SONG_END = pygame.USEREVENT + 1
    
    def play(self,song_name,song_path):
        #Le doy play a la cancion selecionada
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()

        #Obtengo la duracion de la cancion
        try:
            song_obj = pygame.mixer.Sound(song_path)
            self.song_length = song_obj.get_length()
        except:
           self.song_length = 0

        #Actualizo todo los estados
        self.current_file = song_name
        self.playing = True
        self.paused = False
        
    def unpause(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False

    def pause(self):
        if self.playing and not self.paused:
            pygame.mixer.music.pause()
            self.paused = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.song_length = 0
        self.playing = False
        self.paused = False
        self.current_file =  None

    def slide_song(self,target_seconds):
        pygame.mixer.music.play(start = target_seconds)
            
        if self.paused:
            pygame.mixer.music.pause()
    
    def get_song_position(self):
        if self.playing:
            pos = pygame.mixer.music.get_pos() / 1000
            if pos >= 0:
                return pos
            else:
                return 0

    def check_songs_over(self):
        if not pygame.mixer.music.get_busy():
            return True
    
    def volumen(self, value):
        return pygame.mixer.music.set_volume(value)