import cv2
from simple_facerec import SimpleFacerec
import sqlite3 as sl
import time 
from assistant import speak

def cctv(close_callback=None):
    """
    Starts the CCTV camera feed, detects known faces in real-time,
    updates their location and time in the database, and greets recognized users.

    The function attempts to open a camera device, processes video frames to detect faces,
    and displays the video with bounding boxes and names around detected faces.

    Press ESC key to exit the camera feed.
    """

    con = sl.connect('data.db')

    # Initialize face recognizer and load known face encodings from images folder
    sfr = SimpleFacerec()
    sfr.load_encoding_images("images/")

    # Attempt to open camera device with DirectShow backend, trying indices 0 and 1
    cap = None
    for index in [0, 1]:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if cap.isOpened():
            print(f"Camera opened at index {index}")
            break
        else:
            cap.release()
            cap = None
    if cap is None or not cap.isOpened():
        print("Error: Could not open any camera.")
        return

    last_greeted_id = None

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("Failed to grab frame from camera")
            break

        # Detect known faces in the current frame
        face_locations, ids = sfr.detect_known_faces(frame)
        for face_loc, id in zip(face_locations, ids):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            name = ""
            if id == "Unknown":
                color = (0, 0, 200)  # Red color for unknown faces
                name = "Unknown"
            else:
                color = (0, 200, 0)  # Green color for recognized faces
                # Update user's location and time in the database
                query = "UPDATE USER SET location=?, time=? WHERE id=" + id
                data = ('Hostel O', time.time())
                with con:
                    con.execute(query, data)
                # Retrieve user's name from the database
                with con:
                    data = con.execute("SELECT name FROM USER WHERE id=" + id)
                    for row in data:
                        name = row[0]
                print(name)
                # Greet the user if not greeted already
                if last_greeted_id != id:
                    speak("Welcome " + name)
                    last_greeted_id = id
                    cap.release()
                    cv2.destroyAllWindows()
                    if close_callback:
                        close_callback()
                    return
            # Draw name and bounding box on the frame
            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, color, 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 4)

        # Display the frame
        cv2.imshow("Frame", frame)

        # Exit on ESC key press
        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
#cctv()



