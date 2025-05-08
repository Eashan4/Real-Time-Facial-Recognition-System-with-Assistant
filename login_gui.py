import tkinter as tk
from tkinter import messagebox
import cv2
from simple_facerec import SimpleFacerec
from unified_gui import UnifiedGUI
from PIL import Image, ImageTk

class LoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Authentication Login")
        self.root.geometry("400x300")
        self.root.configure(bg="#1f2833")

        self.sfr = SimpleFacerec()
        self.sfr.load_encoding_images("images/")

        self.label = tk.Label(root, text="Please login with your face", font=("Arial", 16), fg="white", bg="#1f2833")
        self.label.pack(pady=20)

        self.login_btn = tk.Button(root, text="Login with Face", command=self.face_login, bg="#c23616", fg="white", font=("Arial", 14))
        self.login_btn.pack(pady=20)

        self.video_label = tk.Label(root)
        self.video_label.pack()

        self.cap = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def face_login(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        ret, frame = self.cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to access camera")
            return

        face_locations, face_names = self.sfr.detect_known_faces(frame)
        if face_names:
            recognized = False
            for name in face_names:
                if name != "Unknown":
                    recognized = True
                    break
            if recognized:
                self.cap.release()
                self.cap = None
                messagebox.showinfo("Login Success", f"Welcome {name}!")
                self.root.destroy()
                self.open_main_gui()
            else:
                messagebox.showerror("Login Failed", "Face not recognized. Please try again.")
        else:
            messagebox.showerror("Login Failed", "No face detected. Please try again.")

    def open_main_gui(self):
        main_root = tk.Tk()
        app = UnifiedGUI(main_root)
        main_root.mainloop()

    def on_closing(self):
        if self.cap is not None:
            self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginGUI(root)
    root.mainloop()
