import streamlit as st
from open_camera import Camera
import cv2
import os
from google.cloud import storage, firestore
import atdata
import feedback
import show as sh

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Insert Google json file"

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = 'web'
if "captured" not in st.session_state:
    st.session_state.captured = False
if "camera_active" not in st.session_state:
    st.session_state.camera_active = False
if "image_count" not in st.session_state:
    st.session_state.image_count = 0
if "image_url" not in st.session_state:
    st.session_state.image_url = None
if "web_next" not in st.session_state:
    st.session_state.web_next=False

# Ensure the necessary directories exist
faces_dir = 'faces'
if not os.path.exists(faces_dir):
    os.makedirs(faces_dir)

detected_faces_dir = 'detected_faces'
if not os.path.exists(detected_faces_dir):
    os.makedirs(detected_faces_dir)

st.set_page_config(
    page_title="V-sight",
    page_icon="v-sight.jpg",
    layout="centered",
    initial_sidebar_state="expanded",
    
)

# Initialize Google Cloud Firestore
db = firestore.Client()



def save_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    return f"https://storage.googleapis.com/{bucket_name}/{destination_blob_name}"

def run_camera():
    # Create an instance of the Camera class
    camera = Camera()
    col1, col2, col3 = st.columns(3)
    # Streamlit UI for camera feed
    frame_slot = st.empty()
    stop_button_placeholder = st.empty()

    

    st.session_state.camera_active = True
    st.session_state.web_next= True
    camera.stop_clicked = False

    # Continuously capture and display video
    while st.session_state.camera_active:
        frame = camera.get_frame()
        if frame is None:
            break

        labels_folder_path = faces_dir  # Path to your labels folder
        labels = camera.load_labels_from_folder(labels_folder_path)

        frame_with_faces, box_detected_faces, count = camera.recognize_faces(frame, labels)
        frame_with_faces = cv2.cvtColor(frame_with_faces, cv2.COLOR_BGR2RGB)
        frame_slot.image(frame_with_faces, channels="RGB", use_column_width=True)

        # Display saved images
        if box_detected_faces and not camera.stop_clicked:
            st.session_state.captured = True
            st.session_state.camera_active = False
            st.session_state.image_count = count
            break  # Stop the camera after detecting and saving faces

        
            

    # Release the camera
    camera.release_camera()
tab1,tab2=st.tabs(["Attendace System","Present List"])
with tab1:
    # Main interface
    if st.session_state.page == 'web':

            st.title("Expogenix Attendance System :newspaper:")
            st.divider()
            

            # Inject the footer HTML and CSS into the Streamlit app
            
            st.markdown("<center><h1>Smile for the camera :)</h1></center>", unsafe_allow_html=True)
            st.markdown("""
                <style>
                div.stButton {text-align:center}
                </style>""", unsafe_allow_html=True)
            button_placeholder = st.empty()
            next_placeholder = st.empty()

            # Initial button to start the camera
            if not st.session_state.camera_active:
                start_button = button_placeholder.button("Start Camera", key="start_button", type="primary")
                if start_button:
                    button_placeholder.empty()  # Remove the start button
                    run_camera()  # Run the camera function

            # Show the next button after capturing
            if st.session_state.web_next:
                next_button = next_placeholder.button("Next", type="primary", key="next_button")
                if next_button:
                    
                    image_path = os.path.join('detected_faces', f"face_{st.session_state.image_count}.jpg")
                    # Save image to Google Cloud Storage
                    gcs_bucket_name = "expogenix_sttendance"  # Replace with your bucket name
                    image_url = save_to_gcs(gcs_bucket_name, image_path, f"face_{st.session_state.image_count}.jpg")
                    st.session_state.image_url = image_url
                    st.session_state.submit_pressed = False
                    
                    st.session_state.page= "atdata"
                    st.rerun()

    # Navigation logic
    if st.session_state.page == 'atdata':
        atdata.data_page(db, st.session_state.image_url, st.session_state.image_count)
    elif st.session_state.page == 'feedback':
        feedback.feedback(db,st.session_state.image_count)
with tab2:
    sh.main()