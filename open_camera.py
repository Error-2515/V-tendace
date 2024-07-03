import cv2
import os

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# OpenCV font settings
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_thickness = 2
count=0
def save_to_firestore(name, roll_no, branch, gimg,db,count,year):
        doc_ref = db.collection("attendance").document(str(count))
        doc_ref.set({
            "name": name,
            "roll_no": roll_no,
            "branch": branch,
            "year":year,
            "image_url": gimg
        }, merge=True)
def save_result(db,result,count,suggest):
    doc_ref=db.collection("attendance").document(str(count))
    doc_ref.update({
        "result": result,
        "Suggestion": suggest
    })
class Camera:
    
    def __init__(self):
        self.vid = cv2.VideoCapture(0)  # Ensure this opens the correct camera
        self.counter = 0  # Initialize a counter for the saved images
        self.stop_clicked = False  # Flag to indicate if the stop button was clicked

    def get_frame(self):
        ret, frame = self.vid.read()
        return frame

    def release_camera(self):
        self.vid.release()

    def load_labels_from_folder(self, folder_path):
        labels = []
        for label in os.listdir(folder_path):
            labels.append(os.path.splitext(label)[0])
        return labels

    def recognize_faces(self, image, labels):
        global count
        if len(image.shape) == 2:  # If image is grayscale, convert to BGR
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        image = cv2.flip(image, 1)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        detected_faces = []
        box_detected_faces = []
        for i, (x, y, w, h) in enumerate(faces):
            face_roi = gray[y:y + h, x:x + w]
            label = labels[i] if i < len(labels) else f"unknown_{i}"
            count += 1

            if not self.stop_clicked:  # Save the image only if stop button was not clicked
                # Save the image
                image_save_path = os.path.join('detected_faces', f"{label}_{count}.jpg")
                cv2.imwrite(image_save_path, image)
                detected_faces.append(image_save_path)
                # Draw rectangle around the face
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # Add label to the detected face
                cv2.putText(image, "Detected: " + label, (x, y - 10), font, font_scale, (255, 0, 0), font_thickness)
                # Save the image with a box around the face
                box_image_save_path = os.path.join('box_detected_faces', f"{label}_{count}.jpg")
                cv2.imwrite(box_image_save_path, image)
                box_detected_faces.append(box_image_save_path)

            

        return image, box_detected_faces, count
