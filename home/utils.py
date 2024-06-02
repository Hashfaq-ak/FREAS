import cv2
from datetime import datetime
from .models import Attendance, Employee

# Function to mark attendance using facial recognition
def mark_attendance_using_facial_recognition():
    # Load the pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Initialize the webcam or camera
    camera = cv2.VideoCapture(0)  # Use 0 for default webcam, you can change it if you have multiple cameras

    while True:
        # Capture frame-by-frame
        ret, frame = camera.read()

        # Convert the captured frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Iterate over detected faces
        for (x, y, w, h) in faces:
            # Extract the detected face region
            face_region = gray_frame[y:y+h, x:x+w]

            # Perform face recognition (implement this part)
            matched_employee = recognize_face(face_region)  # Implement this function

            if matched_employee:
                # Create an attendance record for the matched employee
                attendance_record = Attendance.objects.create(
                    employee=matched_employee,
                    timestamp=datetime.now(),  # Use current timestamp
                    attendance_type='IN'  # Assuming it's for marking in time
                )
                # Save the attendance record
                attendance_record.save()

                # Return a success message
                return "Attendance marked successfully"

        # Display the captured frame
        cv2.imshow('Captured Frame', frame)

        # Check if the user pressed the 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the OpenCV window
    camera.release()
    cv2.destroyAllWindows()

    # If no match is found for any detected face, return a message indicating failure
    return "Face not recognized, attendance not marked"

# Function to recognize the face in the given image region
def recognize_face(face_region):
    # Implement face recognition logic here
    # This function should return the matched employee based on the face recognition algorithm
    # For simplicity, you can return None for now
    return None
