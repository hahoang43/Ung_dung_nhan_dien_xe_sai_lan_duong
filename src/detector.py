from ultralytics import YOLO

class VehicleDetector:
    def __init__(self, model_path='yolov8l.pt'): # <--- Đổi sang bản L (Large)
        print(f"Đang tải model {model_path} (High Accuracy Mode)...")
        self.model = YOLO(model_path)
        # 2: car, 3: motorcycle, 5: bus, 7: truck
        self.vehicle_classes = [2, 3, 5, 7]

    def detect(self, frame):
        """
        Phát hiện xe với cấu hình tối ưu độ chính xác.
        """
        results = self.model(
            frame, 
            verbose=False,
            imgsz=640,        # <--- Tăng độ phân giải nhận diện
            conf=0.25,          # <--- Ngưỡng tin cậy cao hơn
            iou=0.45,          # <--- Lọc trùng lặp
            agnostic_nms=True  # <--- Ngăn chặn 1 xe có 2 class
        )[0]

        detections = []
        
        for box in results.boxes:
            cls_id = int(box.cls[0])
            if cls_id in self.vehicle_classes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                
                # --- (MẸO PHỤ) LỌC THEO KÍCH THƯỚC ---
                # Xe quá nhỏ (ở quá xa) thường nhận diện sai -> Bỏ qua
                w = x2 - x1
                h = y2 - y1
                if w < 30 or h < 30: # Nếu xe nhỏ hơn 30x30 pixel
                    continue 

                detections.append((x1, y1, x2, y2, conf, cls_id))
                
        return detections