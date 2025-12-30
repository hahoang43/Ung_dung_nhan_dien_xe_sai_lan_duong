from ultralytics import YOLO
import cv2

class VehicleDetector:
    def __init__(self, model_path='yolov8n.pt'):
        """
        Khởi tạo model YOLO.
        Nếu chưa có file weights, ultralytics sẽ tự động tải về.
        """
        print(f"Đang tải model {model_path}...")
        self.model = YOLO(model_path)
        # Các class ID của xe cộ trong COCO dataset
        # 2: car, 3: motorcycle, 5: bus, 7: truck
        self.vehicle_classes = [2, 3, 5, 7]

    def detect(self, frame):
        """
        Phát hiện xe trong khung hình.
        Trả về list các bounding box: [(x1, y1, x2, y2, conf, cls_id), ...]
        """
        results = self.model(frame, verbose=False)[0]
        detections = []
        
        for box in results.boxes:
            cls_id = int(box.cls[0])
            if cls_id in self.vehicle_classes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                detections.append((x1, y1, x2, y2, conf, cls_id))
                
        return detections
