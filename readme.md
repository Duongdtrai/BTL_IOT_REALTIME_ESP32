# Real-time Temperature and Humidity Data Logging Web App with ESP32 and Firebase

## Giới Thiệu Đề Tài
Trong thế giới kết nối ngày nay, việc thu thập và truy cập dữ liệu nhiệt độ và độ ẩm theo thời gian thực là vô cùng quan trọng cho nhiều ứng dụng khác nhau. Dự án này đã được thúc đẩy bởi nhu cầu theo dõi môi trường, như theo dõi thời tiết, quản lý điều kiện trong nhà. Chúng tôi đã lấy cảm hứng từ đó tạo ra một web app đơn giản liên quan đến việc thu thập và ghi lại dữ liệu về nhiệt độ và độ ẩm theo thời gian thực rôi từ đó phát triển tính năng tư động bât quạt khi nhiệt độ đo đuợc vuợt quá 35 độ C, đồng thời cũng kết hợp bật/tắt quạt bằng nhận diện cử chỉ bàn tay.

## Ứng Dụng

- **Tự Động Hóa Nhà Thông Minh**:
Dự án này được sử dụng để theo dõi thời tiết trong nhà như hiển thị nhiệt độ và độ ẩm trong phòng. Điều này hữu ích cho việc quyết định liệu có cần bật máy lạnh hoặc máy sưởi trong các phòng riêng lẻ.
Được sử dụng trong các nghiên cứu về khí hậu và môi trường.

## Dụng Cụ Cần Chuẩn Bị
- **ESP32 Board:** Đây là vi điều khiển được sử dụng để thu thập dữ liệu từ cảm biến và gửi lên Firebase.
- **DHT22 Sensor:** Cảm biến này được sử dụng để đo nhiệt độ, độ ẩm.
- **Đèn LED (Tùy Chọn):** Đèn LED có thể được sử dụng để hiển thị trạng thái hoạt động của thiết bị.
- **Dây Cắm và Kết Nối Cần Thiết.**
- **Quạt điện**
- **Camera**

## Công Nghệ Sử Dụng
- Firebase: Dùng làm hệ thống cơ sở dữ liệu dựa trên điện toán đám mây phổ biến để lưu trữ dữ liệu theo thời gian thực..
- ESP32 và Arduino IDE: Được sử dụng để lập trình và điều khiển vi điều khiển ESP32.
- Node.js và Firebase Tools: Sử dụng để cài đặt và quản lý dự án Firebase từ máy tính cục bộ.
- Python: Sử dụng model nhận diện cử chỉ tay bật tắt quạt.

## Các Bước Thực Hiện
1. **Tạo Dự Án và Ứng Dụng trên Firebase:**
   - Tạo một dự án trên Firebase và thiết lập một ứng dụng web để nhận API keys và các thông tin khác.

2. **Xây Dựng Mạch Vật Lý:**
   - Kết nối ESP32 với cảm biến DHT22 và thiết lập các kết nối cần thiết.

3. **Lập Trình ESP32:**
   - Lập trình ESP32 để đọc dữ liệu từ cảm biến và gửi lên Firebase Realtime Database sau khi xác thực người dùng.

4. **Xây Dựng Giao Diện Web (Tùy Chọn):**
   - Xây dựng một giao diện web sử dụng công nghệ như HTML, CSS, và JavaScript để hiển thị dữ liệu nhiệt độ và độ ẩm theo thời gian thực.

5. **Xác Thực và Hiển Thị Dữ Liệu:**
   - Xác thực người dùng sử dụng Firebase Authentication và hiển thị dữ liệu nhiệt độ và độ ẩm trên giao diện web hoặc ứng dụng di động.

6. **Bảo Trì và Theo Dõi:**
   - Đảm bảo rằng hệ thống hoạt động ổn định và kiểm tra định kỳ dữ liệu để đảm bảo tính chính xác.
