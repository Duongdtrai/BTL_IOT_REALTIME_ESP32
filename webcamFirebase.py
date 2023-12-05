import threading
import time
from threading import Event

import cv2
import firebase_admin
import mediapipe as mp
from firebase_admin import credentials, db

# Replace with your Firebase credentials JSON file path
cred = credentials.Certificate(
    "./esp32-temperature-real-time-firebase-adminsdk-4qupr-6012ccbb38.json"
)
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://esp32-temperature-real-time-default-rtdb.asia-southeast1.firebasedatabase.app"
    },
)

# Replace with your Firebase Realtime Database reference
firebase_ref_data_node = db.reference("/your_data_node")
firebase_ref_check_cam = db.reference("/check_cam")

# Global variables
fan = 0
check = 0
exit = Event()


# Function to get data to Firebase
def get_data_from_firebase():
    query = firebase_ref_check_cam.order_by_key().limit_to_last(1)
    # Retrieve the data
    results = query.get()

    # Extract the data from the query result
    for key, value in results.items():
        print("checkcam: ", value.get("value"))
        return int(value.get("value"))


# Function to send data to Firebase
def send_data_to_firebase(value_to_send):
    try:
        firebase_ref_data_node.push(
            {
                "value": value_to_send,
                "timestamp": int(time.time()),  # Add a timestamp if needed
            }
        )
        print("Data sent to Firebase successfully.")
    except Exception as e:
        print(f"Error sending data to Firebase: {e}")


# Function to send data in a separate thread
def send_data_in_thread(value_to_send):
    def send_data():
        try:
            # Simulate data processing
            exit.wait(1)

            # Send data to Firebase
            send_data_to_firebase(value_to_send)
            print("Data sent to Firebase in thread")
        except Exception as e:
            print(f"Error in send_data function: {e}")

    # Create a new thread and run send_data in that thread
    thread = threading.Thread(target=send_data)
    thread.start()


# Khởi tạo đối tượng Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Main loop
# Mở camera
cap = cv2.VideoCapture(0)
print(4)
fan = 0
check = 0
checkOnOff = get_data_from_firebase()

# bật
while cap.isOpened():
    ret, frame = cap.read()

    # Đảo ngược hình ảnh để hiển thị đúng hướng
    frame = cv2.flip(frame, 1)

    # Chuyển đổi màu hình ảnh từ BGR sang RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Nhận diện bàn tay
    results = hands.process(rgb_frame)

    # Vẽ các landmarks và đường trên bàn tay
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Lấy vị trí các ngón tay
            index_tip = hand_landmarks.landmark[
                mp_hands.HandLandmark.INDEX_FINGER_TIP
            ]  # Đầu ngón trỏ
            index_pip = hand_landmarks.landmark[
                mp_hands.HandLandmark.INDEX_FINGER_PIP
            ]  # Đít ngón trỏ

            pinky_tip = hand_landmarks.landmark[
                mp_hands.HandLandmark.PINKY_TIP
            ]  # Đầu ngón út
            pinky_pip = hand_landmarks.landmark[
                mp_hands.HandLandmark.PINKY_PIP
            ]  # Đít ngón út

            middle_tip = hand_landmarks.landmark[
                mp_hands.HandLandmark.MIDDLE_FINGER_TIP
            ]  # Đầu ngón giữa
            middle_pip = hand_landmarks.landmark[
                mp_hands.HandLandmark.MIDDLE_FINGER_PIP
            ]  # Đít ngón giữa

            ring_tip = hand_landmarks.landmark[
                mp_hands.HandLandmark.RING_FINGER_TIP
            ]  # Đầu ngón áp út
            ring_pip = hand_landmarks.landmark[
                mp_hands.HandLandmark.RING_FINGER_PIP
            ]  # Đít ngón áp út

            # Phân loại hình ảnh dựa trên vị trí của ngón tay
            # Nếu ngón tay trỏ cao, đó có thể là biểu hiện của "KÉO" hoặc "BAO"
            if index_tip.y < index_pip.y:
                # Nếu ngón út cao, có thể là "BAO"
                if pinky_tip.y < pinky_pip.y:
                    print("Giấy")
                    if fan == 0:
                        fan = 1
                        check = 1
                # Nếu không thì là "Kéo" hoặc "Dùi"
                elif middle_tip.y < middle_pip.y:
                    print("Kéo")
                    if fan == 1:
                        fan = 0
                        check = 1


    if check and checkOnOff:

        print("fan: ", fan)
        print("check: ", check)

        # Send data to Firebase in a separate thread
        send_data_in_thread(fan)
        check = 0



    # Hiển thị hình ảnh với landmarks và kết quả phân loại
    cv2.imshow("Hand Tracking", frame)

    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord("q"):
        exit.set()
        break
    checkOnOff = get_data_from_firebase()

# Giải phóng tài nguyên
hands.close()
cap.release()
cv2.destroyAllWindows()
