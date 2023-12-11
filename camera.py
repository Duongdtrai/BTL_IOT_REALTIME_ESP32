import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf

# Load the trained model
model = tf.keras.models.load_model("D:\hand_gesture_model.h5")


# Function to preprocess the image for the model
def preprocess_image(frame):
    # Resize the frame to match the input size of the model
    resized_frame = cv2.resize(frame, (224, 224))

    # Normalize pixel values to be between 0 and 1
    normalized_frame = resized_frame / 255.0

    # Expand dimensions to create a batch (required by the model)
    input_data = np.expand_dims(normalized_frame, axis=0)

    return input_data


# Function to handle the model prediction
def handle_prediction(prediction):
    predicted_class = np.argmax(prediction)
    if predicted_class == 0:
        print("Hai gesture detected.")
    elif predicted_class == 1:
        print("Nam gesture detected.")
    # Add more cases for other gestures as needed


# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Open camera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        # Perform hand gesture recognition for the first detected hand (assuming only one hand)
        landmarks = results.multi_hand_landmarks[0].landmark
        # Process the landmarks as needed for your gesture recognition model

        # Preprocess the frame for the model
        processed_frame = preprocess_image(frame)

        # Make predictions using the loaded model
        prediction = model.predict(processed_frame)

        # Handle the model prediction
        handle_prediction(prediction)

    # Display the hand landmarks on the frame
    # if results.multi_hand_landmarks:
    #     for landmarks in results.multi_hand_landmarks:
    #         mp.drawing_utils.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the frame
    cv2.imshow("Hand Tracking", frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
hands.close()
