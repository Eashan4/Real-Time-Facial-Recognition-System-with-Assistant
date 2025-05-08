# Real-Time Facial Recognition Surveillance and Tracking System with Assistant

Connect all CCTV cameras to this system to track someone's live location in a premise using facial recognition. It can be also used to maintain records of people entering a premise using their face instead of bio-metrics/cards/manual Entry.

This system when used with national criminal database can track criminals and prevent mishaps.

---

## Setup Instructions

### 1. Install Required Dependencies

Make sure you have Python 3.6 or higher installed. Then install the required Python packages:

```bash
pip install opencv-python face_recognition pyttsx3 pillow numpy
```

Note: `sqlite3` and `tkinter` are usually included with standard Python installations.

### 2. Database Setup

The project uses an SQLite database `data.db` to store user information.

To create the required `USER` table, run the following Python code or use the provided `data_handling.py` as reference:

```python
import sqlite3 as sl

con = sl.connect('data.db')

with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS USER (
            id INTEGER NOT NULL PRIMARY KEY,
            name TEXT,
            location TEXT,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
```

### 3. Running the Project

Run the login GUI for face authentication first:

```bash
python login_gui.py
```

After successful face authentication, the unified GUI combining the Face Entry System and J.A.R.V.I.S Assistant will launch.

### 4. Features

- Face authentication login to access the system.
- Add users with name, roll number, and face images.
- Start live camera feed to recognize faces and track their location and time.
- Voice assistant (J.A.R.V.I.S) with basic commands and animations.
- Database updates with recognized user location and time.
- Single cohesive GUI with Avengers-themed colors and animations.

---

## Notes

- Ensure your camera is connected and accessible.
- Place user face images in the `images/` folder with filenames matching their roll numbers.
- The system uses facial recognition to identify users in real-time.

---

Developed by Apoorv Mishra
