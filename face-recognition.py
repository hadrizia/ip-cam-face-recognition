import face_recognition
import cv2
import glob, os
import time

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
url = 'https://192.168.130.22:8080/videofeed'
video_capture = cv2.VideoCapture(url)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
suspects_name = []
process_this_frame = True
faces = []
faces_file = "data/faces_file"
faces_names_file = "data/faces_names_file"
total_photos = sum([len(files) for r, d, files in os.walk("./data")])

def check_camera(video_capture):
    return video_capture.read()[1] != None

# Function that load an image and recognize it
def load_and_recognize(image_path, name_suspect):
    print 'Loading image: ' + image_path
    image = face_recognition.load_image_file(image_path)
    fc_encodings = face_recognition.face_encodings(image)

    if len(fc_encodings) > 0:
        faces.append(fc_encodings[0])
        suspects_name.append(name_suspect)

def write_file(file_path, list):
    file = open(file_path, "w")
    for element in list:
        file.write(element)
    file.close

def read_file(file_path):
    file = open(file_path, "r")
    print file
    file.close()

def save_faces():
    if check_camera(video_capture):
        for filename in glob.glob('data/**/*.jpg'):
            suspect_name = os.path.dirname(filename).split('/')[1]
            suspect_name = suspect_name.replace('_', ' ')
            load_and_recognize(filename, suspect_name)

def recognize_image(frame):
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx = 0.25, fy = 0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces(faces, face_encoding, tolerance = 0.6)
            name = "Unknown"

            for i in range(len(match)):
                if match[i]:
                    name = suspects_name[i]

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

save_faces()

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    if(check_camera(video_capture)):
        recognize_image(frame)
    else:
        print 'An error occurred in frame. Please check the camera'
        break

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
