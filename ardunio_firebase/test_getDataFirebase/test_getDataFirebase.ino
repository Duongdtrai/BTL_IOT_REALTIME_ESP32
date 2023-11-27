#include <WiFi.h>
#include <HTTPClient.h>
#include <Firebase_ESP_Client.h>
#include "DHT.h"
#include <Adafruit_BME280.h>
//Provide the token generation process info.
#include "addons/TokenHelper.h"
//Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"
// Thông tin kết nối WiFi
#define WIFI_SSID "PhamTungDuong"
#define WIFI_PASSWORD "0969613858"

// Thông tin dự án Firebase
#define API_KEY "AIzaSyCAx3QAAZCVzX4Swg7TluMLsZEgbNpSUb0"
#define USER_EMAIL "d@gmail.com"
#define USER_PASSWORD "123456"
#define DATABASE_URL "https://esp32-temperature-real-time-default-rtdb.asia-southeast1.firebasedatabase.app/"
// Định nghĩa đối tượng BME280
Adafruit_BME280 bme;  // I2C
float temperature;
float humidity;
float pressure;

// Đối tượng để thực hiện kết nối và truy vấn Firebase
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

void initWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Đang kết nối WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(1000);
  }
  Serial.println(WiFi.localIP());
  Serial.println();
}

unsigned long getTime() {
  time_t now;
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    return 0;
  }
  time(&now);
  return now;
}

void setup() {
  Serial.begin(115200);
  Serial.println("Bắt đầu...");

  // Kết nối WiFi
  initWiFi();

  // Khởi tạo cấu hình thời gian
  configTime(0, 0, "pool.ntp.org");

  // Khởi tạo đối tượng Firebase
  config.api_key = API_KEY;
  auth.user.email = USER_EMAIL;
  auth.user.password = USER_PASSWORD;
  config.database_url = DATABASE_URL;

  Firebase.reconnectWiFi(true);
  fbdo.setResponseSize(4096);
  config.token_status_callback = tokenStatusCallback;

  Firebase.begin(&config, &auth);
}

void loop() {
  // Lấy dữ liệu từ Firebase Realtime Database
  fetchDataFromFirebase();
  delay(5000); // Chờ 5 giây trước khi lấy dữ liệu mới
}

void fetchDataFromFirebase() {
  Serial.println("Pham Tung duong");
  HTTPClient http;
  String url =  String(DATABASE_URL) + "/your_data_node.json"; // Thay đổi thành đường dẫn của bạn

  http.begin(url);

  int httpResponseCode = http.GET();

  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);

    // Đọc nội dung phản hồi
    String payload = http.getString();
    Serial.println("Received data: " + payload);

    // Xử lý dữ liệu nhận được từ Firebase
    processFirebaseData(payload);
  } else {
    Serial.print("Error on HTTP request. Response code: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}

void processFirebaseData(String payload) {
   // Parse chuỗi JSON
  // DynamicJsonDocument doc(1024);
  // deserializeJson(doc, jsonString);

  // // Trích xuất dữ liệu từ JSON
  // const char *dataValue = doc["your-json-field"];
  // Serial.print("Data value from Firebase: ");
  // Serial.println(dataValue);
  // Xử lý dữ liệu JSON nhận được từ Firebase
  FirebaseJson receivedJson;
  receivedJson.setJsonData(payload);

  // Trích xuất giá trị từ JSON
  // int receivedValue = receivedJson.get("value");

  // Hiển thị giá trị nhận được từ Firebase
  // Serial.print(receivedJson.get("value"));
  Serial.print("Received value from Firebase: ");
  // Serial.println(receivedValue);

  // Có thể thực hiện các thao tác khác với giá trị nhận được ở đây
}
