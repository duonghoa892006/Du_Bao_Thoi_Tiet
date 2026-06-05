# Du_Bao_Thoi_Tiet Vi Khí Hậu & Cảnh Báo Sớm Quá Nhiệt Nhà Kính

## 1. Giới thiệu đề tài
Hệ thống sử dụng kit vi điều khiển Arduino Uno R3 kết hợp cảm biến DHT22 để thu thập dữ liệu thời gian thực về nhiệt độ và độ ẩm, truyền qua giao tiếp Serial (Baudrate 9600). Chương trình Python AI đóng vai trò bộ não, sử dụng thuật toán Random Forest Regressor để dự báo vi khí hậu sau 15 phút, từ đó tự động phản hồi lệnh điều khiển LED cảnh báo theo 3 cấp độ (Lý tưởng, Quá nhiệt, Sương giá/Ngập úng).

## 2. Các thành phần mã nguồn
* `train_model.py`: Mã nguồn đọc tập dữ liệu mẫu và huấn luyện mô hình Machine Learning.
* `demo_realtime.py`: Mã nguồn chạy hệ thống thời gian thực, đọc cuộn dòng giảm thiểu độ trễ phản hồi.
* `model_predict_temp.pkl` & `model_predict_humid.pkl`: Các file lưu trữ trọng số mô hình đã huấn luyện.
* `greenhouse_dht22_data.csv`: File dữ liệu ghi nhận cuốn chiếu liên tục.

## 3. Hướng dẫn vận hành
1. Kết nối phần cứng: DHT22 kết nối với chân D2 trên Arduino Uno.
2. Nạp chương trình điều khiển cho mạch Arduino.
3. Khởi chạy file `demo_realtime.py` trên máy tính để bắt đầu giám sát hệ thống.
