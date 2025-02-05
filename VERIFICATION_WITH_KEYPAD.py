import sqlite3
import face_recognition
import time
import pickle
import cv2
import imutils
from imutils.video import VideoStream
from imutils.video import FPS
import RPi.GPIO as GPIO

# Initialize the GPIO for Keypad
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setwarnings(False)


MATRIX = [
    [1, 2, 3, 'A'],
    [4, 5, 6, 'B'],
    [7, 8, 9, 'C'],
    ['*', 0, '#', 'D']
]

ROW = [37, 35, 33, 31]  # ROW pins: physical pin numbers
COL = [29, 23, 21, 19]  # COL pins: physical pin numbers

# Initialize the GPIO pins for the keypad
for j in range(4):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j], 1)

for i in range(4):
    GPIO.setup(ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to read input from the keypad
def read_keypad():
    print("Enter ID using the keypad, press 'D' to confirm.")
    input_sequence = ""
    while True:
        for j in range(4):
            GPIO.output(COL[j], 0)
            for i in range(4):
                if GPIO.input(ROW[i]) == 0:
                    char = MATRIX[i][j]
                    print(char, end='', flush=True)  # Display key on the console
                    if char == 'D':  # If 'D' is pressed, return the input sequence
                        print()  # Move to a new line after the input
                        return input_sequence
                    input_sequence += str(char)
                    time.sleep(0.2)
                    while GPIO.input(ROW[i]) == 0:  # Wait until key is released
                        pass
            GPIO.output(COL[j], 1)

# Function to verify and update the wallet balance
def verify_and_print_wallet(name, user_id, cursor):
    try:
        cursor.execute("SELECT id, wallet FROM CUSTOMERS WHERE name = ?", (name,))
        result = cursor.fetchone()

        if result:
            db_id, wallet = result
            if str(db_id) == str(user_id):
                if wallet < 30:
                    print("Insufficient Balance")
                else:
                    new_balance = wallet - 30
                    cursor.execute("UPDATE CUSTOMERS SET wallet = ? WHERE id = ?", (new_balance, db_id))
                    connection.commit()
                    print(f"Wallet balance updated! New balance: {new_balance}")
            else:
                print("Error: ID does not match the record.")
        else:
            print("Error: Name not found in the database.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Initialize the database connection
connection = sqlite3.connect("CUSTOMERS.db")
cursor = connection.cursor()

# Initialize 'currentname' and 'entered_id' to trigger only when a new person is identified
currentname = "unknown"
entered_id = None

# Load the encodings from the pickle file
encodingsP = "encodings.pickle"
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())

# Initialize the video stream and allow the camera sensor to warm up
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# Start the FPS counter
fps = FPS().start()

# Loop over frames from the video file stream
while True:
    # Grab the frame from the threaded video stream and resize it to 500px
    frame = vs.read()
    frame = imutils.resize(frame, width=500)

    # Detect face locations in the current frame
    boxes = face_recognition.face_locations(frame)

    # Compute the facial embeddings for each face bounding box
    encodings = face_recognition.face_encodings(frame, boxes)
    names = []

    face_recognized = False

    # Loop over the facial embeddings
    for encoding in encodings:
        # Attempt to match each face in the input image to known encodings
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"  # Default to "Unknown" if face is not recognized

        # Check to see if we have found a match
        if True in matches:
            face_recognized = True
            # Find the indexes of all matched faces and count them
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # Loop over the matched indexes and maintain a count for each recognized face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # Determine the recognized face with the largest number of votes
            name = max(counts, key=counts.get)

        # If someone new is identified or currentname changes, ask for ID and verify
        if currentname != name:
            currentname = name
            print(f"Recognized: {currentname}")
            entered_id = read_keypad()  # Get the ID via the keypad
            verify_and_print_wallet(currentname, entered_id, cursor)

        # Add the recognized name to the list of names
        names.append(name)

    # Loop over the recognized faces and draw bounding boxes around them
    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 225), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 255), 2)

    # Display the image to our screen
    cv2.imshow("Facial Recognition is Running", frame)

    key = cv2.waitKey(1) & 0xFF

    # Quit when 'q' key is pressed
    if key == ord("q"):
        break

    # Update the FPS counter
    fps.update()

# Stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# Cleanup and close
cv2.destroyAllWindows()
vs.stop()
connection.close()
GPIO.cleanup()


#sudo -E python VERIFICATION_WITH_KEYPAD.py
