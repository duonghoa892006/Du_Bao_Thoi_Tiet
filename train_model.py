import pandas as pd
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib

CSV_FILE = "greenhouse_dht22_data.csv"
SHIFT_STEPS = 450 

if not os.path.exists(CSV_FILE):
    print(f"[LỖI] Không tìm thấy file dữ liệu {CSV_FILE}. Hãy chạy mạch thu thập dữ liệu trước!")
else:
    df = pd.read_csv(CSV_FILE)
    
    if len(df) < (SHIFT_STEPS + 50):
        print(f"[THÔNG BÁO] Chưa đủ dữ liệu để train. Hiện có {len(df)} mẫu, cần tối thiểu {SHIFT_STEPS + 50} mẫu.")
    else:
        # Tạo nhãn mục tiêu dịch chuỗi (Tương lai 15 phút sau)
        df['Target_Temp'] = df['Temperature'].shift(-SHIFT_STEPS)
        df['Target_Humid'] = df['Humidity'].shift(-SHIFT_STEPS)
        df_ml = df.dropna()
        
        X = df_ml[['Temperature', 'Humidity']]
        
        # Tách tập dữ liệu đánh giá (80% Train, 20% Test)
        X_train_t, X_test_t, y_train_t, y_test_t = train_test_split(X, df_ml['Target_Temp'], test_size=0.2, random_state=42)
        X_train_h, X_test_h, y_train_h, y_test_h = train_test_split(X, df_ml['Target_Humid'], test_size=0.2, random_state=42)
        
        # Huấn luyện mô hình
        model_t = RandomForestRegressor(n_estimators=50, random_state=42)
        model_h = RandomForestRegressor(n_estimators=50, random_state=42)
        
        model_t.fit(X_train_t, y_train_t)
        model_h.fit(X_train_h, y_train_h)
        
        # Đánh giá độ chính xác
        pred_test_t = model_t.predict(X_test_t)
        pred_test_h = model_h.predict(X_test_h)
        
        print("\n" + "="*50)
        print("📊 KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH AI (Ghi vào báo cáo PDF):")
        print(f"🔹 Dự đoán Nhiệt độ -> R2 Score: {r2_score(y_test_t, pred_test_t)*100:.2f}% | MSE: {mean_squared_error(y_test_t, pred_test_t):.4f}")
        print(f"🔹 Dự đoán Độ ẩm    -> R2 Score: {r2_score(y_test_h, pred_test_h)*100:.2f}% | MSE: {mean_squared_error(y_test_h, pred_test_h):.4f}")
        print("="*50)
        
        # Xuất file .pkl [cite: 29]
        joblib.dump(model_t, 'model_predict_temp.pkl')
        joblib.dump(model_h, 'model_predict_humid.pkl')
        print("💾 Đã xuất thành công file 'model_predict_temp.pkl' và 'model_predict_humid.pkl'!")
