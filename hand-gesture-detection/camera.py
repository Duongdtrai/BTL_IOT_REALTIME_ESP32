import threading
import time
from threading import Event

import cv2
import firebase_admin
import mediapipe as mp
import numpy as np
import tensorflow as tf
from firebase_admin import credentials, db

# Thay đổi đường dẫn của tệp tin Firebase credentials JSON theo đường dẫn của bạn
cred = credentials.Certificate(
    "./esp32-temperature-real-time-firebase-adminsdk-4qupr-6012ccbb38.json"
)
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://esp32-temperature-real-time-default-rtdb.asia-southeast1.firebasedatabase.app"
    },
)

# Biến toàn cục
fan = 0
check = 0
exit = Event()

# Thay đổi đường dẫn của Firebase Realtime Database reference theo đường dẫn của bạn
firebase_ref_data_node = db.reference("/your_data_node")
firebase_ref_check_cam = db.reference("/check_cam")

# Tải mô hình đã được đào tạo
model = tf.keras.models.load_model("hand_gesture_model.h5")


# Hàm tiền xử lý ảnh cho mô hình
def preprocess_image(frame):
    # Resize frame để khớp với kích thước đầu vào của mô hình
    resized_frame = cv2.resize(frame, (224, 224))
    # Chuẩn hóa giá trị pixel để nằm trong khoảng từ 0 đến 1
    normalized_frame = resized_frame / 255.0

    # Mở rộng chiều để tạo một batch (yêu cầu bởi mô hình)
    input_data = np.expand_dims(normalized_frame, axis=0)

    return input_data


# Hàm xử lý dự đoán của mô hình
def handle_prediction(prediction):
    predicted_class = np.argmax(prediction)
    return 0 if predicted_class == 0 else 1


# Hàm để nhận dữ liệu từ Firebase
def get_data_from_firebase():
    query = firebase_ref_check_cam.order_by_key().limit_to_last(1)
    # Truy xuất dữ liệu
    results = query.get()

    # Trích xuất dữ liệu từ kết quả truy vấn
    for key, value in results.items():
        # print("checkcam: ", value.get("value"))
        return int(value.get("value"))


# Hàm để gửi dữ liệu đến Firebase
def send_data_to_firebase(value_to_send):
    try:
        firebase_ref_data_node.push(
            {
                "value": value_to_send,
                "timestamp": int(time.time()),  # Thêm timestamp nếu cần
            }
        )
        print("Dữ liệu đã được gửi đến Firebase thành công.")
    except Exception as e:
        print(f"Lỗi khi gửi dữ liệu đến Firebase: {e}")


# Hàm để gửi dữ liệu trong một luồng riêng
def send_data_in_thread(value_to_send):
    def send_data():
        try:
            # Giả lập xử lý dữ liệu
            exit.wait(1)

            # Gửi dữ liệu đến Firebase
            send_data_to_firebase(value_to_send)
            print("Dữ liệu đã được gửi đến Firebase trong luồng")
        except Exception as e:
            print(f"Lỗi trong hàm send_data: {e}")

    # Tạo một luồng mới và chạy send_data trong luồng đó
    thread = threading.Thread(target=send_data)
    thread.start()


# Khởi tạo MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Mở camera
cap = cv2.VideoCapture(0)
fan = 0
check = 0
checkOnOff = get_data_from_firebase()

while cap.isOpened():
    ret, frame = cap.read()

    # Lật frame theo chiều ngang để hiển thị ở chế độ xem tự sướng sau này
    frame = cv2.flip(frame, 1)

    # Chuyển đổi hình ảnh BGR sang RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Xử lý frame với MediaPipe Hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        # Thực hiện nhận diện cử chỉ tay cho bàn tay đầu tiên được phát hiện (giả sử chỉ có một bàn tay)
        landmarks = results.multi_hand_landmarks[0].landmark
        # Xử lý các điểm đánh dấu cần thiết cho mô hình nhận diện cử chỉ tay của bạn

        # Tiền xử lý frame cho mô hình
        processed_frame = preprocess_image(frame)

        # Đưa ra dự đoán sử dụng mô hình đã tải
        prediction = model.predict(processed_frame)

        # Xử lý dự đoán của mô hình
        # 0 là "two", 1 là "five"
        if handle_prediction(prediction) == 1:
            if fan == 0:
                print("Giấy")
                fan = 1
                check = 1
        elif handle_prediction(prediction) == 0:
            if fan == 1:
                print("Kéo")
                fan = 0
                check = 1

    if check and checkOnOff:
        print("fan: ", fan)
        print("check: ", check)
        # Gửi dữ liệu đến Firebase trong một luồng riêng
        send_data_in_thread(fan)
        check = 0

    cv2.imshow("Theo dõi Bàn tay", frame)

    # Thoát khỏi vòng lặp khi nhấn 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        exit.set()
        break
    checkOnOff = get_data_from_firebase()

# Giải phóng tài nguyên
hands.close()
cap.release()
cv2.destroyAllWindows()
hands.close()
