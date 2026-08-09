import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image
from functionalities.files_manager import filesManager
from functionalities.sound_manager import soundManager

ctk.set_appearance_mode('system')
ctk.set_default_color_theme("blue")


class GUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.audio = soundManager()
        self.files = filesManager()

        self.title('Music Player')
        self.geometry('650x460')
        self.resizable(False, False)

        self.isShuffle = False
        self.isDragging = False
        self.seek_offset = 0

        self.load_grid()
        self.load_icons()

        self.UI()
        self.key_binding()
        self.update_playlist_ui()
        self.song_progress()

    def UI(self):
        # 1. Topframe - Manejador de directorio
        self.top_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.top_frame.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=15, pady=(10, 5)
        )

        self.open_folder_btn = ctk.CTkButton(self.top_frame,text='Open folder', command=self.files.open_folder, width=100)
        self.open_folder_btn.pack(side='right', padx=5)

        self.change_folder_btn = ctk.CTkButton(self.top_frame,text='Change folder',command=self.change_folder,width=100)
        self.change_folder_btn.pack(side='right', padx=5)

        # 2. Songframe
        self.song_frame = ctk.CTkFrame(self, corner_radius=10)
        self.song_frame.grid(row=1, column=0, sticky="nsew", padx=(15, 5), pady=5)
        self.song_frame.pack_propagate(False)

        self.song_name = ctk.StringVar(value="<Not selected>")
        self.song_lbl = ctk.CTkLabel(self.song_frame,textvariable=self.song_name,font=("Arial", 13, "bold"),fg_color="#1f538d",corner_radius=6,wraplength=340,)
        self.song_lbl.pack(fill='both', expand=True, padx=15, pady=15)

        # 3. Playlistframe - Scrollbar de canciones
        self.list_frame = ctk.CTkFrame(self, corner_radius=10)
        self.list_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 15), pady=5)

        self.playlist = tk.Listbox(self.list_frame,bg="#2b2b2b", fg='white',selectbackground='#3aafa9', selectforeground='black', borderwidth=0,highlightthickness=0, activestyle="none")
        self.scroll_bar = ctk.CTkScrollbar(self.list_frame, command=self.playlist.yview)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5)

        self.playlist.config(yscrollcommand=self.scroll_bar.set)
        self.playlist.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 4. Btnframe (Controles inferiores)
        self.btn_frame = ctk.CTkFrame(self, corner_radius=10)
        self.btn_frame.grid(row=2, column=0, columnspan=2, sticky='ew', padx=15, pady=(5, 15))

        # Frame de Tiempo (Izquierda: Actual | Derecha: Total)
        self.time_box = ctk.CTkFrame(self.btn_frame, fg_color="transparent")
        self.time_box.pack(fill="x", padx=25, pady=(10, 0))

        self.curr_time_lbl = ctk.CTkLabel(self.time_box, text="0:00", font=("Arial", 11))
        self.curr_time_lbl.pack(side="left")

        self.total_time_lbl = ctk.CTkLabel(self.time_box, text="0:00", font=("Arial", 11)        )
        self.total_time_lbl.pack(side="right")

        # Barra de progreso
        self.progress_bar = ctk.CTkSlider(self.btn_frame,from_=0, to=100, number_of_steps=1000, height=6, button_length=10, button_corner_radius=5, fg_color="#333333", progress_color="#3aafa9", button_color="#ffffff", button_hover_color="#3aafa9",)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=20, pady=(2, 10))

        self.progress_bar.bind( "<Button-1>", lambda event: setattr(self, 'isDragging', True))
        self.progress_bar.bind("<ButtonRelease-1>", self.slide_song)

        # Fila de Botones y Volumen
        self.controls_box = ctk.CTkFrame(self.btn_frame, fg_color="transparent")
        self.controls_box.pack(fill="x", padx=20, pady=(0, 10))

        # Contenedor central para botones de reproducción
        self.buttons_subframe = ctk.CTkFrame(self.controls_box, fg_color="transparent")
        self.buttons_subframe.pack(side="left", expand=True)

        self.shuffle_song_btn = ctk.CTkButton(self.buttons_subframe,text='',image=self.shuffle_icon,fg_color='#e63946', command=self.shuffle_song,width=40)
        self.shuffle_song_btn.pack(side="left", padx=2)

        self.prev_song_btn = ctk.CTkButton(self.buttons_subframe,text='',image=self.prev_icon,fg_color='#e63946',command=self.prev_song, width=40)
        self.prev_song_btn.pack(side="left", padx=2)

        self.btn_action = ctk.CTkButton(self.buttons_subframe,text='',image=self.play_icon,fg_color='orange',command=self.toggle_play,width=45)
        self.btn_action.pack(side="left", padx=2)

        self.next_song_btn = ctk.CTkButton(self.buttons_subframe,text='',image=self.next_icon,fg_color='#e63946',command=self.next_song,width=40)
        self.next_song_btn.pack(side="left", padx=2)

        self.stop_btn = ctk.CTkButton(self.buttons_subframe,text='',image=self.stop_icon,fg_color='#e63946',command=self.stop_music,width=40)
        self.stop_btn.pack(side="left", padx=2)

        # Sección de Volumen a la derecha
        self.volumen_subframe = ctk.CTkFrame(self.controls_box, fg_color='transparent')
        self.volumen_subframe.pack(side="right")

        self.volumen_icon_lbl = ctk.CTkLabel(self.volumen_subframe, text='', image=self.volume_icon)
        self.volumen_icon_lbl.pack(side='left', padx=(0, 5))

        self.volumen_slider = ctk.CTkSlider(self.volumen_subframe,from_=0,to=1,width=100,command=self.audio.volumen)
        self.volumen_slider.pack(side="left")

    # Función auxiliar para convertir segundos a formato MM:SS
    def format_time(self, seconds):
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}:{secs:02d}"

    # Actualizo los estados de la playlist en la UI
    def update_playlist_ui(self):
        self.playlist.delete(0, tk.END)
        for songs in self.files.songs:
            self.playlist.insert(tk.END, songs)

    def update_currently_playing(self):
        self.playlist.selection_clear(0, tk.END)
        if self.files.current_index != -1:
            self.playlist.selection_set(self.files.current_index)
            self.playlist.activate(self.files.current_index)

    # Funcionalidades
    def toggle_play(self, event=None):
        selected_file = self.playlist.curselection()

        if not selected_file and self.audio.current_file is None:
            return

        if selected_file:
            selection = self.playlist.get(selected_file[0])
        else:
            selection = self.audio.current_file

        if self.audio.current_file != selection:
            song_path = self.files.get_song_path(selection)
            self.files.set_song_index(selection)
            self.audio.play(selection, song_path)
            self.song_name.set(selection)
            self.seek_offset = 0
            self.btn_action.configure(
                image=self.pause_icon, text='', fg_color='orange'
            )

        elif self.audio.playing and not self.audio.paused:
            self.audio.pause()
            self.btn_action.configure(
                image=self.play_icon, text='', fg_color='Orange'
            )

        elif self.audio.paused:
            self.audio.unpause()
            self.btn_action.configure(
                image=self.pause_icon, text='', fg_color='Orange'
            )

    def stop_music(self, event=None):
        if self.audio.playing:
            self.audio.stop_music()
            self.progress_bar.set(0)
            self.seek_offset = 0
            self.curr_time_lbl.configure(text="0:00")
            self.total_time_lbl.configure(text="0:00")
            self.btn_action.configure(
                image=self.play_icon, text='', fg_color='Orange'
            )

    def next_song(self, event=None):
        if self.audio.playing or self.audio.paused:
            song_name = self.files.next_song()

            if song_name:
                self.audio.play(song_name, self.files.get_song_path(song_name))
                self.seek_offset = 0
                self.song_name.set(song_name)
                self.update_currently_playing()
                self.btn_action.configure(
                    image=self.pause_icon, text='', fg_color='Orange'
                )

    def prev_song(self, event=None):
        if self.audio.playing or self.audio.paused:
            song_name = self.files.prev_song()

            if song_name:
                self.audio.play(song_name, self.files.get_song_path(song_name))
                self.seek_offset = 0
                self.song_name.set(song_name)
                self.update_currently_playing()
                self.btn_action.configure(
                    image=self.pause_icon, text='', fg_color='Orange'
                )

    def shuffle_song(self):
        self.files.shuffle_song(self.isShuffle, self.audio.current_file)

        self.isShuffle = not self.isShuffle
        self.update_playlist_ui()
        self.update_currently_playing()

        if self.isShuffle:
            self.shuffle_song_btn.configure(text='', fg_color='orange')
        else:
            self.shuffle_song_btn.configure(text='', fg_color='#e63946')

    def change_folder(self):
        new_drt = filedialog.askdirectory(title='Open a songs directory')

        if new_drt:
            self.files.set_folder(new_drt)
            self.stop_music()
            self.isShuffle = False
            self.shuffle_song_btn.configure(text='', fg_color='#e63946')
            self.update_playlist_ui()
            self.song_name.set("<Not selected>")

    # Sigue el progreso de la canción y actualiza los tiempos
    def song_progress(self):
        if (
            self.audio.playing
            and not self.audio.paused
            and self.audio.song_length > 0
            and not self.isDragging
        ):
            current_song = self.seek_offset + self.audio.get_song_position()
            percentage = (current_song / self.audio.song_length) * 100
            self.progress_bar.set(percentage)

            # Actualización de etiquetas MM:SS
            self.curr_time_lbl.configure(
                text=self.format_time(current_song)
            )
            self.total_time_lbl.configure(
                text=self.format_time(self.audio.song_length)
            )

            if self.audio.check_songs_over():
                self.next_song()

        self.after(1000, self.song_progress)

    def slide_song(self, event):
        if (
            self.audio.playing or self.audio.paused
        ) and self.audio.song_length > 0:
            percentage = self.progress_bar.get()
            target_seconds = (percentage / 100) * self.audio.song_length
            self.seek_offset = target_seconds
            self.audio.slide_song(target_seconds)

            # Actualizar label mientras se arrastra
            self.curr_time_lbl.configure(
                text=self.format_time(target_seconds)
            )

        self.isDragging = False

    def load_icons(self):
        self.play_icon = ctk.CTkImage(
            Image.open(self.files.icons_dir / "play-icon.png")
        )
        self.pause_icon = ctk.CTkImage(
            Image.open(self.files.icons_dir / "pause-icon.png")
        )
        self.next_icon = ctk.CTkImage(
            Image.open(self.files.icons_dir / "next-icon.png")
        )
        self.prev_icon = ctk.CTkImage(
            Image.open(self.files.icons_dir / "prev-icon.png")
        )
        self.stop_icon = ctk.CTkImage(
            Image.open(self.files.icons_dir / "stop-icon.png")
        )
        self.shuffle_icon = ctk.CTkImage(
            Image.open(self.files.icons_dir / "shuffle-icon.png")
        )
        self.volume_icon = ctk.CTkImage(
            Image.open(self.files.icons_dir / "volume-icon.png")
        )

    def key_binding(self):
        self.bind("<space>", self.toggle_play)
        self.bind("<Double-1>", self.toggle_play)
        self.bind("<F7>", self.stop_music)
        self.bind("<F8>", self.prev_song)
        self.bind("<F9>", self.toggle_play)
        self.bind("<F10>", self.next_song)
        self.bind("<Control-o>", self.files.open_folder)

    def load_grid(self):
        self.grid_columnconfigure(0, weight=70)
        self.grid_columnconfigure(1, weight=30)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)