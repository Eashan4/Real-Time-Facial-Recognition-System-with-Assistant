import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import shutil
import sqlite3 as sl
import webbrowser
import os
from main import cctv
from assistant import speak
from PIL import Image

class UnifiedGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Avengers Face Entry and J.A.R.V.I.S Assistant")
        self.root.geometry("900x700")
        self.root.configure(bg="#0b0c10")

        self.con = sl.connect('data.db')

        # Title Label
        self.title_label = Label(self.root, text="Avengers Face Entry and J.A.R.V.I.S Assistant", font=("Segoe UI", 24, "bold"), bg="#0b0c10", fg="#ffcc00")
        self.title_label.pack(pady=15)

        # Main Frame
        self.main_frame = Frame(self.root, bg="#1f2833")
        self.main_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # Face Entry Frame
        self.face_frame = Frame(self.main_frame, bg="#1f2833", bd=2, relief=RIDGE)
        self.face_frame.place(x=10, y=10, width=430, height=660)

        self.face_title = Label(self.face_frame, text="Face Entry System", font=("Segoe UI", 20, "bold"), bg="#1f2833", fg="#ffcc00")
        self.face_title.grid(row=0, column=0, columnspan=4, pady=10)

        # Name
        self.name_text = StringVar()
        self.name_label = Label(self.face_frame, text='Name', font=('Segoe UI', 14, 'bold'), bg="#1f2833", fg="#ffcc00")
        self.name_label.grid(row=1, column=0, sticky=W, padx=10)
        self.name_entry = Entry(self.face_frame, textvariable=self.name_text, font=('Segoe UI', 12))
        self.name_entry.grid(row=1, column=1, columnspan=3, sticky=EW, padx=10, pady=5)

        # Roll No
        self.roll_text = StringVar()
        self.roll_label = Label(self.face_frame, text='Roll No', font=('Segoe UI', 14, 'bold'), bg="#1f2833", fg="#ffcc00")
        self.roll_label.grid(row=2, column=0, sticky=W, padx=10)
        self.roll_entry = Entry(self.face_frame, textvariable=self.roll_text, font=('Segoe UI', 12))
        self.roll_entry.grid(row=2, column=1, columnspan=3, sticky=EW, padx=10, pady=5)

        # Image Upload
        self.img_label = Label(self.face_frame, text='Select Image', font=('Segoe UI', 14, 'bold'), bg="#1f2833", fg="#ffcc00")
        self.img_label.grid(row=3, column=0, sticky=W, padx=10, pady=(20, 5))
        self.upload_btn = Button(self.face_frame, text='Upload Files', command=self.upload_file, bg="#c23616", fg="white", font=('Segoe UI', 12, 'bold'))
        self.upload_btn.grid(row=3, column=1, columnspan=3, sticky=EW, padx=10, pady=5)

        # Output Label
        self.out_label = Label(self.face_frame, text='', font=('Segoe UI', 14, 'bold'), bg="#1f2833", fg="#ffcc00")
        self.out_label.grid(row=10, column=0, columnspan=4, pady=10)

        # Start Camera Button
        self.cam_btn = Button(self.face_frame, text='Start Camera', command=self.start_camera, bg="#c23616", fg="white", font=('Segoe UI', 14, 'bold'))
        self.cam_btn.grid(row=11, column=0, columnspan=4, pady=20)

        # Jarvis Assistant Frame
        self.jarvis_frame = Frame(self.main_frame, bg="#1a1a1a", bd=2, relief=RIDGE)
        self.jarvis_frame.place(x=460, y=10, width=420, height=660)

        self.jarvis_title = Label(self.jarvis_frame, text="J.A.R.V.I.S Assistant", font=("Segoe UI", 20, "bold"), bg="#1a1a1a", fg="#ffcc00")
        self.jarvis_title.pack(pady=10)

        # Jarvis Command Entry
        self.command_entry = Entry(self.jarvis_frame, width=40, bg="#0b0c10", fg="#ffcc00", font=('Segoe UI', 16, 'bold'))
        self.command_entry.pack(padx=10, pady=20)

        # Jarvis Buttons Frame
        self.buttons_frame = Frame(self.jarvis_frame, bg="#1a1a1a")
        self.buttons_frame.pack(pady=10)

        self.google_btn = Button(self.buttons_frame, text="Open Google", bg="#0b0c10", fg="#ffcc00", width=15, command=self.open_google)
        self.google_btn.grid(row=0, column=0, padx=5, pady=5)

        self.youtube_btn = Button(self.buttons_frame, text="Open YouTube", bg="#0b0c10", fg="#ffcc00", width=15, command=self.open_youtube)
        self.youtube_btn.grid(row=0, column=1, padx=5, pady=5)

        self.command_btn = Button(self.buttons_frame, text="Execute Command", bg="#0b0c10", fg="#ffcc00", width=32, command=self.execute_command)
        self.command_btn.grid(row=1, column=0, columnspan=2, pady=10)

        # Animation Canvas
        self.canvas = Canvas(self.jarvis_frame, width=380, height=300, bg="#0b0c10", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.shape = self.canvas.create_oval(10, 10, 60, 60, fill="#c23616")
        self.xspeed = 5
        self.yspeed = 5

        self.shape2 = self.canvas.create_oval(100, 100, 150, 150, fill="#c23616")
        self.xspeed2 = 7
        self.yspeed2 = 7

        self.animate()

    def animate(self):
        self.canvas.move(self.shape, self.xspeed, self.yspeed)
        pos = self.canvas.coords(self.shape)
        if pos[3] >= 300 or pos[1] <= 0:
            self.yspeed = -self.yspeed
        if pos[2] >= 380 or pos[0] <= 0:
            self.xspeed = -self.xspeed

        self.canvas.move(self.shape2, self.xspeed2, self.yspeed2)
        pos = self.canvas.coords(self.shape2)
        if pos[3] >= 300 or pos[1] <= 0:
            self.yspeed2 = -self.yspeed2
        if pos[2] >= 380 or pos[0] <= 0:
            self.xspeed2 = -self.xspeed2

        self.root.after(20, self.animate)

    def upload_file(self):
        f_types = [('Image Files', '*.jpg *.png')]
        filenames = filedialog.askopenfilenames(filetypes=f_types)
        if not filenames:
            return
        col = 1
        row = 4
        for f in filenames:
            img = Image.open(f)
            try:
                roll = int(self.roll_text.get())
            except ValueError:
                self.out_label.config(text="Roll No must be an integer", fg="red")
                speak("Roll number must be an integer")
                return
            # Check if roll already exists
            with self.con:
                data = self.con.execute("SELECT id FROM USER WHERE id=?", (roll,))
                exists = data.fetchone()
            if exists:
                self.out_label.config(text=f"Roll No {roll} already exists. Updating record.", fg="orange")
                speak(f"Roll number {roll} already exists. Updating record.")
                sql = 'UPDATE USER SET name=?, location=? WHERE id=?'
                data = (self.name_text.get(), 'Main Gate', roll)
                with self.con:
                    self.con.execute(sql, data)
            else:
                sql = 'INSERT INTO USER (id, name, location) values(?, ?, ?)'
                data = (roll, self.name_text.get(), 'Main Gate')
                with self.con:
                    self.con.execute(sql, data)
            shutil.copy(img.filename, 'images/' + str(roll) + '.jpg')

            img = img.resize((100, 100))
            img = ImageTk.PhotoImage(img)
            e1 = Label(self.face_frame, image=img)
            e1.image = img
            e1.grid(row=row, column=col)
            if col == 3:
                row += 1
                col = 1
            else:
                col += 1
            self.out_label.config(text="Added to DB", fg="#ffcc00")
            speak(f"Added {self.name_text.get()} to database")

    def start_camera(self):
        speak("Starting camera")
        cctv()

    def open_google(self):
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    def open_youtube(self):
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    def execute_command(self):
        query = self.command_entry.get().lower()
        if 'open file' in query:
            speak("Which file sir?")
            self.open_file_dialog()
        elif 'shutdown' in query:
            speak("Shutting down the computer")
            os.system("shutdown now -h")
        elif 'open stackoverflow' in query:
            speak("Opening Stack Overflow")
            webbrowser.open("https://www.stackoverflow.com")
        elif 'open website' in query:
            speak("Which website sir?")
            self.open_website_dialog()
        elif 'open google' in query:
            self.open_google()
        elif 'open youtube' in query:
            self.open_youtube()
        elif 'copy code' in query:
            speak("Which file sir?")
            self.copy_code_dialog()
        elif 'exit' in query or 'quit' in query:
            speak("Goodbye sir, have a good day")
            self.root.quit()
        else:
            speak("Sorry sir, I cannot do this")

    def open_file_dialog(self):
        d = Toplevel(self.root)
        d.configure(bg="#0b0c10")
        e = Entry(d, bg="#0b0c10", fg="#ffcc00", width=20)
        e.pack()

        def open_file():
            os.system(e.get())
            speak("Opening " + e.get())

        s = Button(d, bg="#0b0c10", fg="#ffcc00", width=10, activeforeground="#c23616", activebackground="#1f2833",
                   text="Open it", command=open_file)
        s.pack()

    def open_website_dialog(self):
        d = Toplevel(self.root)
        d.configure(bg="#0b0c10")
        e = Entry(d, bg="#0b0c10", fg="#ffcc00", font=('arial', 18, 'bold'), width=20)
        e.pack()

        def open_web():
            webbrowser.open("https://" + e.get() + ".com")
            speak("Opening " + e.get())

        s = Button(d, bg="#0b0c10", fg="#ffcc00", width=10, activeforeground="#c23616", activebackground="#1f2833",
                   text="Open it", command=open_web)
        s.pack()

    def copy_code_dialog(self):
        d = Toplevel(self.root)
        d.configure(bg="#0b0c10")
        e = Entry(d, bg="#0b0c10", font=('arial', 18, 'bold'), fg="#ffcc00", width=20)
        e.pack()

        def open_code():
            try:
                with open(e.get(), "r") as file:
                    content = file.read()
                speak(content)
            except Exception:
                speak("Sorry sir, I could not read the file.")

        s = Button(d, bg="#0b0c10", fg="#ffcc00", width=10, activeforeground="#c23616", activebackground="#1f2833",
                   text="Open it", command=open_code)
        s.pack()

if __name__ == "__main__":
    root = Tk()
    app = UnifiedGUI(root)
    root.mainloop()
