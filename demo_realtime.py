import serial
import time
import csv
import os
import pandas as pd
import joblib

COM_PORT = 'COM3'       # Sửa cổng COM của bạn
BAUD_RATE = 9600
CSV_FILE = "greenhouse_dht22_data.csv"

# Kiểm tra xem đã có file mô hình được huấn luyện từ trước chưa [cite: 29]
if not os.path.exists('model_predict_temp.pkl') or not os.path.exists('model_predict_humid.pkl'):
    print("[LỖI] Không tìm thấy file mô hình .pkl! Hãy chạy file train_model.py trước để tạo mô hình.")
else:
    # Tải bộ não AI đã học sẵn vào hệ thống demo
    model_temp = joblib.load('model_predict_temp.pkl')
    model_humid = joblib.load('model_predict_humid.pkl')
    print("🧠 [THÀNH CÔNG] Đã nạp bộ não AI (.pkl). Hệ thống sẵn sàng dự đoán!")

    try:
        arduino = serial.Serial(port=COM_PORT, baudrate=BAUD_RATE, timeout=1)
        time.sleep(2)
        print(f"[ĐÃ KẾT NỐI] Đang chạy Demo thời gian thực từ cổng {COM_PORT}...\n")
        
        while True:
            if arduino.in_waiting > 0:
                raw_data = arduino.readline().decode('utf-8').strip()
                
                if "Temp:" in raw_data and "Humid:" in raw_data:
                    try:
                        parts = raw_data.split('|')
                        current_t = float(parts[0].split(':')[1].strip())
                        current_h = float(parts[1].split(':')[1].strip())
                        
                        # 1. Ghi lưu trữ dữ liệu thực tế vào file CSV
                        now_timestamp = time.time()
                        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            writer.writerow([now_timestamp, current_t, current_h])
                        
                        print(f"\n[REAL-TIME INPUT] Temp: {current_t}°C | Humid: {current_h}%")
                        
                        # 2. Sử dụng mô hình đã tải để dự đoán tương lai cuốn chiếu
                        current_features = pd.DataFrame([[current_t, current_h]], 
                                                        columns=['Temperature', 'Humidity'])
                        
                        pred_t = model_temp.predict(current_features)[0]
                        pred_h = model_humid.predict(current_features)[0]
                        
                        print(f"🔮 [AI DỰ BÁO 15P SAU] T: {pred_t:.1f}°C | H: {pred_h:.1f}%")
                        
                        # Phát cảnh báo sớm ra màn hình dựa trên kết quả dự báo
                        if pred_t > 35.0 and pred_h < 50.0:
                            print("🚨 TRẠNG THÁI: Khô hại / Quá nhiệt (LOẠI 2)!")
                        elif pred_t < 15.0 or pred_h > 90.0:
                            print("⚠️ TRẠNG THÁI: Sương giá / Ngập úng (LOẠI 3)!")
                        else:
                            print("✅ TRẠNG THÁI: Lý tưởng (LOẠI 1).")
                            
                        time.sleep(2)
                        
                    except Exception as err:
                        print(f"[LỖI XỬ LÝ]: {err}")
                        
    except serial.SerialException:
        print(f"[LỖI] Không kết nối được với cổng {COM_PORT}. Hãy kiểm tra dây cáp Arduino!")
    except KeyboardInterrupt:
        print("\n[DỪNG] Đã tắt chương trình demo an toàn.")
    finally:
        if 'arduino' in locals() and arduino.is_open:
            arduino.close()