import cv2
from .utils import is_point_in_polygon, draw_polygon, draw_text

class LaneMonitor:
    def __init__(self, lanes_config):
        """
        lanes_config: List các dict định nghĩa làn đường.
        Ví dụ:
        [
            {
                "name": "Làn xe máy",
                "polygon": [(0, 0), (100, 0), (100, 100), (0, 100)],
                "allowed_classes": [3], # Chỉ cho phép xe máy (ID 3)
                "color": (0, 255, 0)
            },
            {
                "name": "Làn ô tô",
                "polygon": [...],
                "allowed_classes": [2, 5, 7], # Car, Bus, Truck
                "color": (255, 0, 0)
            }
        ]
        """
        self.lanes = lanes_config
        self.violations = []

    def check_violations(self, detections, frame):
        """
        Kiểm tra các xe được phát hiện có đi sai làn không.
        detections: [(x1, y1, x2, y2, conf, cls_id), ...]
        """
        current_violations = []
        
        # Vẽ các làn đường trước
        for lane in self.lanes:
            draw_polygon(frame, lane['polygon'], color=lane['color'], label=lane['name'])

        for (x1, y1, x2, y2, conf, cls_id) in detections:
            # Lấy điểm trung tâm dưới đáy của bounding box (đại diện vị trí bánh xe)
            center_x = int((x1 + x2) / 2)
            center_y = int(y2)
            vehicle_point = (center_x, center_y)

            # Vẽ bounding box xe
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
            cv2.circle(frame, vehicle_point, 5, (0, 0, 255), -1)

            # Kiểm tra xe thuộc làn nào
            in_any_lane = False
            for lane in self.lanes:
                if is_point_in_polygon(vehicle_point, lane['polygon']):
                    in_any_lane = True
                    # Nếu loại xe không nằm trong danh sách cho phép của làn này -> Vi phạm
                    if cls_id not in lane['allowed_classes']:
                        violation_text = f"SAI LAN: {lane['name']}"
                        draw_text(frame, violation_text, (x1, y1 - 10), color=(0, 0, 255))
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                        current_violations.append({
                            "bbox": (x1, y1, x2, y2),
                            "lane": lane['name'],
                            "class_id": cls_id
                        })
                    else:
                        # Đi đúng làn
                        draw_text(frame, "DUNG LAN", (x1, y1 - 10), color=(0, 255, 0))
                    break # Giả sử các làn không chồng lấn, tìm thấy 1 làn là dừng
            
            if not in_any_lane:
                # Xe không nằm trong làn nào được định nghĩa (có thể bỏ qua hoặc cảnh báo)
                pass

        return frame, current_violations
