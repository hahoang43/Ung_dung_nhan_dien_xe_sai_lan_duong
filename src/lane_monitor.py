import cv2
from .utils import is_point_in_polygon, draw_polygon, draw_text

class LaneMonitor:
    def __init__(self, lanes_config):
        self.lanes = lanes_config
        # Tạo bộ nhớ lưu ID các xe vi phạm cho từng làn
        # Cấu trúc: { 'Tên Làn': {id1, id2, ...}, ... }
        self.violation_memory = {lane['name']: set() for lane in lanes_config}

    def check_violations(self, detections, frame):
        """
        detections: List [(x1, y1, x2, y2, track_id, conf, cls_id), ...]
        """
        current_violations = [] # Chỉ dùng để vẽ khung đỏ trong frame hiện tại
        
        # 1. Vẽ vùng làn đường
        for lane in self.lanes:
            draw_polygon(frame, lane['polygon'], color=lane['color'], label=lane['name'])

        # 2. Duyệt qua các xe
        for (x1, y1, x2, y2, track_id, conf, cls_id) in detections:
            center_point = (int((x1 + x2) / 2), int(y2))

            for lane in self.lanes:
                if is_point_in_polygon(center_point, lane['polygon']):
                    # Nếu xe nằm trong làn
                    if cls_id not in lane['allowed_classes']:
                        # === SAI LÀN ===
                        lane_name = lane['name']
                        
                        # A. Lưu ID vào bộ nhớ (Set sẽ tự loại bỏ ID trùng)
                        self.violation_memory[lane_name].add(track_id)

                        # B. Vẽ cảnh báo
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        cv2.circle(frame, center_point, 5, (0, 0, 255), -1)
                        draw_text(frame, f"SAI LAN: {lane_name} (ID: {track_id})", (x1, y1 - 10), color=(0, 0, 255))
                        
                        current_violations.append(track_id)
                    else:
                        # === ĐÚNG LÀN ===
                        # (Tùy chọn: Uncomment dòng dưới nếu muốn hiện ID xe đi đúng)
                        # draw_text(frame, f"ID: {track_id}", (x1, y1 - 10), color=(255, 255, 255))
                        pass
                    break # Đã tìm thấy làn thì dừng check làn khác

        # 3. Hiển thị tổng số lượng vi phạm lên góc màn hình
        y_offset = 50
        cv2.putText(frame, "THONG KE VI PHAM:", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        for lane_name, id_set in self.violation_memory.items():
            count = len(id_set)
            text = f"- {lane_name}: {count} xe"
            cv2.putText(frame, text, (10, y_offset + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            y_offset += 30

        return frame, current_violations