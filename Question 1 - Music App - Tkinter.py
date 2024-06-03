###############################################################################################
                                # HIT137 SOFTWARE NOW – Assignment 3 #

# Lecturer name: Abhijith Beeravolu
# Group members: 
#        - Son Lam Nguyen (Justin) (Student ID: s377342) 
#        - Chirag Dudhat (Student ID: S374835)
# GitHub group link: https://github.com/son-lam-nguyen-s377342/HIT137_SOFTWARENOW_Assignment3.git

###############################################################################################

import tkinter as tk
from tkinter import filedialog
from pygame import mixer
from PIL import Image, ImageTk

# Base class for the music player
class MusicPlayer:
    def __init__(self):
# Encapsulation: storing private state variables
        self._current_track = None
        mixer.init()

    def load_track(self, track_path):
        self._current_track = track_path
        mixer.music.load(track_path)
    
    def play(self):
        mixer.music.play()

    def stop(self):
        mixer.music.stop()

    def pause(self):
        mixer.music.pause()

    def resume(self):
        mixer.music.unpause()

# Multiple inheritance, inheriting from both MusicPlayer and tk.Tk
class MusicApp(MusicPlayer, tk.Tk):
    def __init__(self):
        MusicPlayer.__init__(self)
        tk.Tk.__init__(self)
        self.title("Music Player")
        self.geometry("400x300")
        self.set_background(r'C:\Users\lamng\Downloads\Question 1 - Music App\music.jpg')
        self.create_widgets()
    
    # Overriding Tkinter methods
    def create_widgets(self):
        self.track_label = tk.Label(self, text="No track loaded", font=("Arial", 16))
        self.track_label.pack(pady=20)

        self.load_button = tk.Button(self, text="Load Track", font=("Arial", 14), command=self.load_track_action)
        self.load_button.pack(pady=10)

        self.play_button = tk.Button(self, text="Play", font=("Arial", 14), command=self.play)
        self.play_button.pack(pady=10)

        self.pause_button = tk.Button(self, text="Pause", font=("Arial", 14), command=self.pause)
        self.pause_button.pack(pady=10)

        self.resume_button = tk.Button(self, text="Resume", font=("Arial", 14), command=self.resume)
        self.resume_button.pack(pady=10)

        self.stop_button = tk.Button(self, text="Stop", font=("Arial", 14), command=self.stop)
        self.stop_button.pack(pady=10)
    
    def set_background(self, image_path):
        try:
            self.background_image = Image.open(image_path)
            self.background_photo = ImageTk.PhotoImage(self.background_image)
            self.background_label = tk.Label(self, image=self.background_photo)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error setting background: {e}")

    # Polymorphism methods inherited from MusicPlayer and overridden in the context of MusicApp
    def load_track_action(self):
        track_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if track_path:
            self.load_track(track_path)
            self.track_label.config(text=track_path.split("/")[-1])

    # Decorator to demonstrate functionality extension
    @staticmethod
    def log_action(func):
        def wrapper(*args, **kwargs):
            print(f"Action performed: {func.__name__}")
            return func(*args, **kwargs)
        return wrapper

    @log_action
    def play(self):
        super().play()

    @log_action
    def stop(self):
        super().stop()

    @log_action
    def pause(self):
        super().pause()

    @log_action
    def resume(self):
        super().resume()

if __name__ == "__main__":
    app = MusicApp()

    # Polymorphism
    app.mainloop()
