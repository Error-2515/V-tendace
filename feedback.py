import streamlit as st
import cv2
import mediapipe as mp
import open_camera as oc

def feedback(db,count):
    # Initialize mediapipe
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

    # Set up Streamlit
    st.title("Feedback Time!!!")
    st.subheader("please do give us your opinin about if the event was good or bad usingyour hands")
    st.text("thunms up - Good")
    st.text("thumbs down - could be better")

    if "camera_active" not in st.session_state:
        st.session_state.camera_active = False

    if "result" not in st.session_state:
        st.session_state.result = ""

    if "submit_pressed" not in st.session_state:
        st.session_state.submit_pressed = False

    def run_camera():
        cap = cv2.VideoCapture(0)
        stframe = st.empty()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Flip the image horizontally for a later selfie-view display
            frame = cv2.flip(frame, 1)
            
            # Convert the BGR image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame and detect hands
            result = hands.process(rgb_frame)
            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Get landmark points
                    landmarks = hand_landmarks.landmark
                    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
                    thumb_mcp = landmarks[mp_hands.HandLandmark.THUMB_MCP]
                    index_finger_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                    # Calculate the angle or positions to determine the gesture
                    if thumb_tip.y < thumb_mcp.y < index_finger_tip.y:
                        st.session_state.result = "Good"
                        st.session_state.camera_active = False
                        break
                    elif thumb_tip.y > thumb_mcp.y > index_finger_tip.y:
                        st.session_state.result = "Could be better"
                        st.session_state.camera_active = False
                        break
            
            # Display the frame
            stframe.image(frame, channels="BGR")

            if not st.session_state.camera_active:
                break

        cap.release()
        cv2.destroyAllWindows()

    if not st.session_state.camera_active:
        if st.button("Start Camera"):
            st.session_state.camera_active = True
            run_camera()

    if st.session_state.result:
        st.write(f"Result: {st.session_state.result}")
        recom=st.text_input("please write any suggestions you have for future events:")
        if not st.session_state.submit_pressed:
            if st.button("Submit"):
                oc.save_result(db=db, count=count, result=st.session_state.result,suggest=recom)
                st.session_state.clear()
                
                st.rerun()


