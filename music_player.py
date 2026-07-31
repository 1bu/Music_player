import tkinter as tk
from tkinter import filedialog
import os
import subprocess
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame


def main():
    formats = ".mp3"
    songs = []

    try:
        pygame.mixer.init()
    except pygame.error as e:
        print('Audio initialization failed',e)
        return

    #Busco y creo la carpeta con la musica si esta no existe
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MUSIC_DIR = os.path.join(BASE_DIR, 'Music')

    if not os.path.isdir(MUSIC_DIR):
        os.mkdir(MUSIC_DIR)

    for files in os.listdir(MUSIC_DIR):
        if files.lower().endswith(formats):
            songs.append(files)

    UI(songs, MUSIC_DIR)
    return 0

def get_song_path(song_name,state):
    return os.path.join(state['current_directory'], song_name)

def play_song(state,song_name,current_song,btn_action):
    song_path = get_song_path(song_name,state)
    current_song.set(song_name)
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

    state['current_file'] = song_name
    state["playing"] = True
    state['paused'] = False
    btn_action.config(text="Pause", bg='Orange')

#Funcionalidades
def toggle_play(btn_action, state, playlist,current_song):
    selected_file = playlist.curselection()

    if not selected_file and state['current_playing'] is None:
        return
    
    if selected_file:
        selection = playlist.get(selected_file[0])
    else:
        selection = state['current_file']

    #Si la cancion seleccionada es diferente
    if state["current_file"] != selection:
        play_song(state, selection, current_song,btn_action)

    #Si la cancion seleccionada es la misma -> se pause
    elif state['playing'] and not state['paused'] :
        pygame.mixer.music.pause()
        state['paused'] = True
        btn_action.config(text="Play", bg='Orange')

    #Si la cancion es la misma y esta pausada -> se reanuda
    elif state['paused']:
        pygame.mixer.music.unpause()
        state['paused'] = False
        btn_action.config(text="Pause", bg='Orange')

def stop_music(state):
    if state:
        pygame.mixer.music.stop()
        state['playing'] = False
        state['paused'] = False
        state['current_file'] =  None
        
def next_song(state, playlist,current_song,btn_action):
    if state['playing']:
        next_selected = playlist.curselection()
        next_selected = next_selected[0] + 1

        if next_selected >= playlist.size():
            next_selected = 0

        #Cambio la cancion seleccionada
        playlist.selection_clear(0, tk.END)
        playlist.selection_set(next_selected)
        playlist.activate(next_selected)

        next_song_name = playlist.get(next_selected)
        play_song(state,next_song_name, current_song, btn_action)

def prev_song(state, playlist, current_song,btn_action):
    if state['playing']:
        prev_selected = playlist.curselection()
        prev_selected = prev_selected[0] - 1

        if prev_selected < 0:
            prev_selected = playlist.size() - 1

        #Cambio la cancion seleccionada
        playlist.selection_clear(0, tk.END)
        playlist.selection_set(prev_selected)
        playlist.activate(prev_selected)

        prev_song_name = playlist.get(prev_selected)
        play_song(state,prev_song_name, current_song, btn_action)

def open_folder(base_dir,state):
    try:   
        return os.startfile(state['current_directory'])
    except:
        return subprocess.Popen(['xdg-open',state['current_directory']])

def change_folder(playlist,state):
    new_drt = (filedialog.askdirectory(title='Open a songs directory'))
    
    if new_drt:
        state['current_directory'] = new_drt

        playlist.delete(0, tk.END)
        formats = ".mp3"
        for file in os.listdir(new_drt):
            if file.lower().endswith(formats):
                playlist.insert(tk.END,file)


def UI(files,base_dir):
    state = {
        "playing": False,
        "paused": False,
        "current_file":None,
        "current_directory": base_dir
        }    

    #Canvas
    canvas = tk.Tk()
    canvas.title('Music Player')
    canvas.geometry('600x400')
    canvas.resizable(0,0)
    canvas.config(bg='black')

    #Frames
    song_frame = tk.LabelFrame(canvas, text = "Current Song", bg = 'lightblue', width = 400, height = 280)
    song_frame.place(x=0,y=0)

    btn_frame = tk.LabelFrame(canvas, bg = 'lightblue', width = 400, height = 120)
    btn_frame.place(y=280)

    list_frame = tk.LabelFrame(canvas, text = 'Song List', bg = 'RoyalBlue')
    list_frame.place(x=400, y=0, width = 200, height = 400)

    current_song = tk.StringVar(canvas, value='<Not selected>')

    #Listbox 
    #Scrollbar de canciones
    playlist = tk.Listbox(list_frame, selectbackground='gold')
    scroll_bar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
    scroll_bar.pack(side = tk.RIGHT, fill = tk.BOTH)

    playlist.config(yscrollcommand=scroll_bar.set)
    scroll_bar.config(command=playlist.yview)
    playlist.pack(fill=tk.BOTH, padx=5, pady=5)

    for index,songs in enumerate(files):
        playlist.insert(index,songs)
    
    #Cancion sonando
    song_lbl = tk.Label(song_frame, textvariable = current_song, bg = 'Goldenrod', width = 25)
    song_lbl.place(x=20, y=20)

    #Botones de accion
    btn_action = tk.Button(btn_frame, text='Play', bg= 'Orange', width = 8, command=lambda:toggle_play(btn_action, state, playlist, current_song))
    btn_action.place(x = 110, y = 10)

    stop_btn = tk.Button(btn_frame, text='Stop', bg= 'Aqua', width = 8, command=lambda:stop_music(state))
    stop_btn.place(x = 205, y = 10)

    next_song_btn = tk.Button(btn_frame, text='->', bg= 'Aqua', width = 8, command=lambda:next_song(state, playlist,current_song,btn_action))
    next_song_btn.place(x = 300, y = 10)

    prev_song_btn = tk.Button(btn_frame, text='<-', bg= 'Aqua', width = 8, command=lambda:prev_song(state,playlist,current_song,btn_action))
    prev_song_btn.place(x = 15, y = 10)

    #Manejador de directorio
    open_folder_btn = tk.Button(btn_frame, text='Open folder', bg='Aqua', width = 18, command=lambda:open_folder(base_dir,state))
    open_folder_btn.place(x=20, y = 60)

    change_folder_btn = tk.Button(btn_frame, text='Change folder', bg='Aqua', width = 18,command=lambda:change_folder(playlist,state))
    change_folder_btn.place(x=205, y = 60)

    canvas.mainloop()

main()