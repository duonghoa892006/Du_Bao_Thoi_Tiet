import pandas as pd
import numpy as np
import time

CSV_FILE = "greenhouse_dht22_data.csv"

# 1. Thiết lập 1500 mốc thời gian (mỗi mốc cách nhau 2 giây)
num_samples = 1500
timestamps = time.time() - np.arange(num_samples) * 2

# 2. Tạo dữ liệu Nhiệt độ giả lập (Biến thiên hình sin từ 16°C đến 38°C)
base_temp = 27 + 11 * np.sin(np.linspace(0, 6 * np.pi, num_samples))
noise_temp = np.random.normal(0, 0.4, num_samples) # Nhiễu môi trường thực tế
temperature = np.round(base_temp + noise_temp, 1)

# 3. Tạo dữ liệu Độ ẩm giả lập (Ngược pha với nhiệt độ, biến thiên từ 40% đến 92%)
base_humid = 66 - 24 * np.sin(np.linspace(0, 6 * np.pi, num_samples))
noise_humid = np.random.normal(0, 0.8, num_samples)
humidity = np.round(np.clip(base_humid + noise_humid, 20, 100), 1)

# 4. Gộp thành cấu trúc bảng dữ liệu
df_synthetic = pd.DataFrame({
    "Timestamp": timestamps[::-1], # Sắp xếp thời gian từ cũ đến mới
    "Temperature": temperature,
    "Humidity": humidity
})

# 5. Ghi đè file CSV mới tinh để mồi cho AI học
df_synthetic.to_csv(CSV_FILE, index=False, encoding='utf-8')

print("="*50)
print(f"✅ [THÀNH CÔNG] Đã tự động tạo {num_samples} mẫu dữ liệu giả lập vi khí hậu!")
print(f"📊 Dải nhiệt độ sinh ra: {temperature.min()}°C -> {temperature.max()}°C")
print(f"📊 Dải độ ẩm sinh ra: {humidity.min()}% -> {humidity.max()}%")
print("📁 File 'greenhouse_dht22_data.csv' đã sẵn sàng cho AI học tập.")
print("="*50)