import threading
import time

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
firebase_ref = db.reference("/your_data_node")

# Global variables
red_led = "0"
green_led = "0"
fan = "0"
str_value = ""
check = 0


# Function to send data to Firebase
def send_data_to_firebase(value_to_send):
    try:
        firebase_ref.push(
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
            # Simulate data processing (replace this with your actual logic)
            time.sleep(0.5)

            # Send data to Firebase
            send_data_to_firebase(value_to_send)
            print("Data sent to Firebase in thread")
        except Exception as e:
            print(f"Error in send_data function: {e}")

    # Create a new thread and run send_data in that thread
    thread = threading.Thread(target=send_data)
    thread.start()


# Function to convert decimal to binary
def decimal_to_binary(decimal_number):
    binary_number = bin(decimal_number)[2:]  # Skip the '0b' prefix
    binary_number = binary_number.rjust(10, "0")
    return binary_number


# Function to convert binary to decimal
def binary_to_decimal(binary_number):
    # decimal_number = int(binary_number, 2)
    # return decimal_number
    return 1


# Khởi tạo đối tượng Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()


# Main function to process data
def process_data():
    global red_led, green_led, fan, str_value, check

    for i in range(5):
        # Simulate getting data (replace this with your actual data retrieval logic)
        a = 123  # Replace this with your data retrieval logic

        # Convert to binary
        str_value = decimal_to_binary(a)

        # Store old value
        temp = str_value

        # Assign values to global variables
        red_led = str_value[7]
        green_led = str_value[9]
        fan = str_value[5]
        check = 0

        # Create delay or perform other processing if needed
        time.sleep(0.1)


# Main loop
# Mở camera
cap = cv2.VideoCapture(0)
print(4)
a = int(1)
str = decimal_to_binary(a)
red_led = str[7]
green_led = str[9]
fan = str[5]
check = 0
temp = ""
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
                    if red_led == "0":
                        red_led = "1"
                        check = 1
                # Nếu không thì là "Kéo" hoặc "Dùi"
                else:
                    if middle_tip.y < middle_pip.y:
                        print("Kéo")
                        if fan == "0":
                            fan = "1"
                            check = 1
                    else:
                        print("Dùi")
                        if green_led == "0":
                            green_led = "1"
                            check = 1
            # Ngược lại, có thể là biểu hiện của "BÚA"
            else:
                print("Búa")
                if red_led == "1" or green_led == "1":
                    red_led = "0"
                    green_led = "0"
                    fan = "0"
                    check = 1

    if check:
        # str_value = (
        #     str_value[:5] + fan + str_value[6] + red_led + str_value[8] + green_led
        # )
        data = binary_to_decimal("abc")

        # Send data to Firebase in a separate thread
        send_data_in_thread(data)

        # Process data as needed
        process_data()

    # Hiển thị hình ảnh với landmarks và kết quả phân loại
    cv2.imshow("Hand Tracking", frame)

    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Giải phóng tài nguyên
hands.close()
cap.release()
cv2.destroyAllWindows()
