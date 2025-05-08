import random
import tkinter    
from tkinter import *
import datetime
import pyttsx3
import os
import time
import subprocess
import webbrowser
import ctypes
from tkinter import _tkinter
from PIL import ImageTk,Image

engine = pyttsx3.init()

def speak(audio):
    """
    Uses pyttsx3 engine to speak the given audio string.
    """
    engine.say(audio)
    engine.runAndWait()

def wish():
    """
    Greets the user based on the current time of day.
    """
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        speak("Good morning sir")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon sir")
    else:
        speak("Good evening sir")

class JarvisAssistant:
    """
    A GUI assistant class named J.A.R.V.I.S with basic commands and animations.
    """
    def __init__(self, window):
        self.window = window
        self.window.configure(bg='#0b0c10')  # Dark background color
        self.SET_WIDTH = 800
        self.SET_HEIGHT = 700
        self.window.title("J.A.R.V.I.S")

        # Removed background image for Avengers theme

        self.canvas = tkinter.Canvas(self.window, width=self.SET_WIDTH, height=self.SET_HEIGHT, bg='#0b0c10', highlightthickness=0)
        self.canvas.pack()

        self.create_widgets()
        self.animate()

    def create_widgets(self):
        """
        Creates buttons and entry widgets for the assistant GUI with Avengers theme.
        """
        self.btn_google = Button(self.window, text="Open Google", bg='#c23616', fg="white", width=20,
                                 activeforeground="#ffcc00", activebackground="#1f2833", command=self.open_google)
        self.btn_google.pack(padx=10, pady=10)

        self.btn_youtube = Button(self.window, text="Open Youtube", bg='#c23616', fg="white", width=20,
                                  activeforeground="#ffcc00", activebackground="#1f2833", command=self.open_youtube)
        self.btn_youtube.pack(padx=10, pady=10)

        self.btn_command = Button(self.window, bg='#c23616', fg="white", width=20, activeforeground="#ffcc00",
                                  activebackground="#1f2833", text="Command", command=self.command)
        self.btn_command.pack(padx=10, pady=10)

        self.ques = Entry(self.window, width=40, bg="#0b0c10", fg="gold", font=('arial', 18, 'bold'), insertbackground='gold')
        self.ques.pack(padx=10, pady=20)

        self.shape = self.canvas.create_oval(10, 10, 60, 60, fill="#c23616")
        self.xspeed = random.randrange(1, 20)
        self.yspeed = random.randrange(1, 20)

        self.shape2 = self.canvas.create_oval(10, 10, 60, 60, fill="#c23616")
        self.xspeed2 = random.randrange(1, 20)
        self.yspeed2 = random.randrange(1, 20)

    def animate(self):
        """
        Animates two blue ovals bouncing within the canvas boundaries.
        """
        self.canvas.move(self.shape, self.xspeed, self.yspeed)
        pos = self.canvas.coords(self.shape)
        if pos[3] >= self.SET_HEIGHT or pos[1] <= 0:
            self.yspeed = -self.yspeed
        if pos[2] >= self.SET_WIDTH or pos[0] <= 0:
            self.xspeed = -self.xspeed

        self.canvas.move(self.shape2, self.xspeed2, self.yspeed2)
        pos = self.canvas.coords(self.shape2)
        if pos[3] >= self.SET_HEIGHT or pos[1] <= 0:
            self.yspeed2 = -self.yspeed2
        if pos[2] >= self.SET_WIDTH or pos[0] <= 0:
            self.xspeed2 = -self.xspeed2

        self.window.after(10, self.animate)

    def open_google(self):
        """
        Opens Google in the default web browser and speaks confirmation.
        """
        speak("Ok sir, I will open Google")
        webbrowser.open("https://www.google.com")

    def open_youtube(self):
        """
        Opens YouTube in the default web browser and speaks confirmation.
        """
        speak("Ok sir, I will open YouTube")
        webbrowser.open("https://www.youtube.com")

    def command(self):
        """
        Processes the command entered in the entry widget and executes corresponding actions.
        """
        query = self.ques.get().lower()
        if 'open file' in query:
            speak("Which file sir?")
            self.open_file_dialog()
        elif 'shutdown' in query:
            speak("Ok sir, I will shutdown the computer")
            os.system("shutdown now -h")
        elif 'open stackoverflow' in query:
            speak("Ok sir, I will open Stack Overflow website")
            webbrowser.open("https://www.stackoverflow.com")
        elif 'open website' in query:
            speak("Which website sir?")
            self.open_website_dialog()
        elif 'open google' in query:
            self.open_google()
        elif 'open youtube' in query:
            self.open_youtube()
        elif 'copy code' in query:
            speak("Of which file sir?")
            self.copy_code_dialog()
        elif 'exit' in query or 'quit' in query:
            speak("Goodbye sir, have a good day")
            self.window.quit()
        else:
            speak("Sorry sir, I cannot do this")

    def open_file_dialog(self):
        """
        Opens a dialog to enter a file path and executes the file.
        """
        d = Toplevel(self.window)
        d.configure(bg="black")
        e = Entry(d, bg="black", fg="white", width=20)
        e.pack()

        def open_file():
            os.system(e.get())
            speak("Ok sir, I will open " + e.get())

        s = Button(d, bg="black", font=('arial', 18, 'bold'), fg="white", width=10,
                   activeforeground="grey", activebackground="black", text="Open it", command=open_file)
        s.pack()

    def open_website_dialog(self):
        """
        Opens a dialog to enter a website name and opens it in the browser.
        """
        d = Toplevel(self.window)
        d.configure(bg="black")
        e = Entry(d, bg="black", fg="white", font=('arial', 18, 'bold'), width=20)
        e.pack()

        def open_web():
            webbrowser.open("https://" + e.get() + ".com")
            speak("Ok sir, I will open " + e.get())

        s = Button(d, bg="black", fg="white", width=10, activeforeground="grey", activebackground="black",
                   text="Open it", command=open_web)
        s.pack()

    def copy_code_dialog(self):
        """
        Opens a dialog to enter a filename and reads its content aloud.
        """
        d = Toplevel(self.window)
        d.configure(bg="black")
        e = Entry(d, bg="black", font=('arial', 18, 'bold'), fg="white", width=20)
        e.pack()

        def open_code():
            try:
                with open(e.get(), "r") as file:
                    content = file.read()
                speak(content)
            except Exception as ex:
                speak("Sorry sir, I could not read the file.")
        s = Button(d, bg="black", fg="white", width=10, activeforeground="grey", activebackground="black",
                   text="Open it", command=open_code)
        s.pack()

if __name__ == "__main__":
    wish()
    root = Tk()
    assistant = JarvisAssistant(root)
    root.mainloop()
