import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import shutil
import sqlite3 as sl
from main import *

con = sl.connect('data.db')

class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.defaultForeground = self["foreground"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = '#ffd700'  # brighter golden hover color
        self['foreground'] = '#0b0c10'  # dark text on hover

    def on_leave(self, e):
        self['background'] = self.defaultBackground
        self['foreground'] = self.defaultForeground

class AnimatedTabBar(Frame):
    def __init__(self, master, tabs, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.tabs = tabs
        self.buttons = []
        self.active_index = 0
        self.indicator = Canvas(self, height=3, bg='#0b0c10', highlightthickness=0)
        self.indicator.pack(side=BOTTOM, fill=X)
        self.create_tabs()
        self.animate_indicator()

    def create_tabs(self):
        for i, tab in enumerate(self.tabs):
            btn = HoverButton(self, text=tab, bg='#1f2833', fg='gold', bd=0, padx=25, pady=12,
                              activebackground='#1f2833', activeforeground='#ffcc00',
                              font=('Segoe UI', 12, 'bold'),
                              command=lambda i=i: self.select_tab(i))
            btn.pack(side=LEFT, padx=10, pady=5)
            self.buttons.append(btn)
        self.update_active_tab()

    def select_tab(self, index):
        self.active_index = index
        self.update_active_tab()
        self.animate_indicator()
        # Call the callback for tab change if exists
        if hasattr(self.master, 'on_tab_change'):
            self.master.on_tab_change(index)

    def update_active_tab(self):
        for i, btn in enumerate(self.buttons):
            if i == self.active_index:
                btn.config(fg='#ffcc00')
            else:
                btn.config(fg='gold')

    def animate_indicator(self):
        self.indicator.delete("all")
        btn = self.buttons[self.active_index]
        x1 = btn.winfo_x()
        x2 = x1 + btn.winfo_width()
        self.indicator.create_rectangle(x1, 0, x2, 3, fill='#ffcc00', outline='#ffcc00')
        self.after(100, self.animate_indicator)

class AvengerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Avengers Face Entry System')
        self.geometry("600x400")
        self.configure(bg='#0b0c10')  # Dark background color

        # Removed background image for custom Avengers theme

        # Removed tab bar as per user request
        # self.tabs = ['Add User', 'Start Camera', 'About']
        # self.tab_bar = AnimatedTabBar(self, self.tabs, bg='#1f2833')
        # self.tab_bar.pack(side=TOP, fill=X)

        # Status bar at the bottom
        self.status_bar = Label(self, text="Welcome to Avengers Face Entry System", bd=1, relief=SUNKEN, anchor=W,
                                bg='#0b0c10', fg='gold', font=('Segoe UI', 11, 'bold'))
        self.status_bar.pack(side=BOTTOM, fill=X)

        self.frames = {}
        self.create_frames()
        # Show only Add User frame filling the window
        self.frames[0].pack(fill=BOTH, expand=True)

    def create_frames(self):
        # Frame for Add User
        frame1 = Frame(self, bg='#1f2833', bd=2, relief=RIDGE)
        self.frames[0] = frame1

        # Name
        self.name_text = StringVar()
        name_label = Label(frame1, text='Name', font=('Segoe UI', 14, 'bold'), fg='gold', bg='#1f2833', pady=10)
        name_label.grid(row=0, column=0, sticky=W, padx=15, pady=15)
        self.name_entry = Entry(frame1, textvariable=self.name_text, bg='#0b0c10', fg='white', insertbackground='gold', font=('Segoe UI', 12))
        self.name_entry.grid(row=0, column=1, padx=15, pady=15)

        # Roll No
        self.roll_text = StringVar()
        roll_label = Label(frame1, text='Roll NO', font=('Segoe UI', 14, 'bold'), fg='gold', bg='#1f2833')
        roll_label.grid(row=0, column=2, sticky=W, padx=15, pady=15)
        self.roll_entry = Entry(frame1, textvariable=self.roll_text, bg='#0b0c10', fg='white', insertbackground='gold', font=('Segoe UI', 12))
        self.roll_entry.grid(row=0, column=3, padx=15, pady=15)

        # Image upload
        img_label = Label(frame1, text='Select Image', font=('Segoe UI', 14, 'bold'), fg='gold', bg='#1f2833', pady=10)
        img_label.grid(row=1, column=0, sticky=W, padx=15, pady=15)
        upload_btn = HoverButton(frame1, text='Upload Files', command=self.upload_file, bg='#e84118', fg='white', font=('Segoe UI', 12, 'bold'))
        upload_btn.grid(row=1, column=1, padx=15, pady=15)

        # Output label
        self.out = Label(frame1, text='', font=('Segoe UI', 14, 'bold'), fg='gold', bg='#1f2833')
        self.out.grid(row=7, column=1, padx=15, pady=15)

        # Start Camera button on Add User page
        start_cam_btn = HoverButton(frame1, text='Start Camera', command=lambda: cctv(close_callback=self.destroy), bg='#e84118', fg='white', font=('Segoe UI', 12, 'bold'))
        start_cam_btn.grid(row=8, column=1, padx=15, pady=15, sticky=W)

        frame1.pack(fill=BOTH, expand=True)

        # Frame for Start Camera
        frame2 = Frame(self, bg='#1f2833', bd=2, relief=RIDGE)
        self.frames[1] = frame2
        # Removed Start Camera button from Add User page as per user request
        # start_cam_btn = HoverButton(frame2, text='Start Camera', command=cctv, bg='#e84118', fg='white', font=('Segoe UI', 14, 'bold'))
        # start_cam_btn.grid(row=0, column=0, padx=20, pady=20)

        frame2.pack(fill=BOTH, expand=True)

        # Frame for About
        frame3 = Frame(self, bg='#1f2833', bd=2, relief=RIDGE)
        self.frames[2] = frame3

        about_label = Label(frame3, text="Avengers Face Entry System\nVersion 1.0\nDeveloped by Your Name", 
                            font=('Segoe UI', 16, 'bold'), fg='gold', bg='#1f2833', justify=CENTER)
        about_label.pack(pady=30)

        close_btn = HoverButton(frame3, text='Close', command=self.quit, bg='#e84118', fg='white', font=('Segoe UI', 14, 'bold'))
        close_btn.pack(pady=20)

        frame3.pack(fill=BOTH, expand=True)

        # Frame for Start Camera
        frame2 = Frame(self, bg='#1f2833')
        self.frames[1] = frame2
        start_cam_btn = HoverButton(frame2, text='Start Cam', command=cctv, bg='#c23616', fg='white')
        start_cam_btn.grid(row=0, column=0, padx=10, pady=10)

    def show_frame(self, index):
        for f in self.frames.values():
            f.pack_forget()
        frame = self.frames[index]
        frame.pack(fill=BOTH, expand=True)

    # Removed on_tab_change method as tab bar is removed
    # def on_tab_change(self, index):
    #     self.show_frame(index)

    def clear_text(self, im, but):
        self.name_entry.delete(0, END)
        self.roll_entry.delete(0, END)
        self.out.config(text="")
        im.config(image='')
        but.destroy()

    def upload_file(self):
        """
        Handles uploading of image files, inserts user data into the database,
        copies images to the images folder, and updates the GUI with the uploaded images.
        """
        f_types = [('Image Files', '*.jpg *.png')]   # type of files to select 
        filename = filedialog.askopenfilename(multiple=True, filetypes=f_types)
        col = 1
        row = 3
        for f in filename:
            img = Image.open(f)
            try:
                roll = int(self.roll_text.get())
            except ValueError:
                self.out.config(text="Roll No must be an integer")
                return
            sql = 'INSERT INTO USER (id, name, location) values(?, ?, ?)'
            data = (roll, self.name_text.get(), 'Main Gate')
            with con:
                con.execute(sql, data)
            shutil.copy(img.filename, 'images/' + str(roll) + '.jpg')

            img = img.resize((100, 100))
            img = ImageTk.PhotoImage(img)
            e1 = Label(self.frames[0], image=img)
            e1.grid(row=row, column=col)
            e1.image = img
            e1['image'] = img

            self.out.grid(row=7, column=1)
            b2 = HoverButton(self.frames[0], text='Add New', command=lambda e1=e1, b2=None: self.clear_text(e1, b2), bg='#c23616', fg='white')
            b2.grid(row=8, column=1)
            if col == 3:
                row += 1
                col = 1
            else:
                col += 1

if __name__ == "__main__":
    app = AvengerGUI()
    app.mainloop()
