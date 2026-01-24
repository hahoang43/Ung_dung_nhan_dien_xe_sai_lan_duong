import cv2
import numpy as np

class LaneDrawer:
    def __init__(self, window_name="Lane Setup"):
        self.window_name = window_name
        self.current_points = []
        self.done = False

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Click chuột trái: Thêm điểm
            self.current_points.append((x, y))
            print(f"Điểm: ({x}, {y})")

        elif event == cv2.EVENT_RBUTTONDOWN:
            # Click chuột phải: Xóa điểm vừa vẽ (Undo)
            if self.current_points:
                self.current_points.pop()

    def get_lane_polygon(self, frame, lane_name):
        """
        Hàm này mở cửa sổ để người dùng vẽ 1 làn đường cụ thể.
        Trả về list các điểm [(x,y), ...]
        """
        self.current_points = []
        self.done = False
        
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_callback)

        print(f"\n--- BẮT ĐẦU VẼ: {lane_name} ---")
        print("1. Click CHUỘT TRÁI để chọn các góc của làn đường.")
        print("2. Nhấn phím 'n' (Next) để hoàn thành làn này.")
        print("3. Nhấn phím 'r' (Reset) để vẽ lại từ đầu.")

        while not self.done:
            display_img = frame.copy()

            # Hướng dẫn trên màn hình
            cv2.putText(display_img, f"VEX LAN: {lane_name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(display_img, "Click: Them diem | 'n': Xong | 'r': Ve lai", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Vẽ các điểm và đường nối
            if len(self.current_points) > 0:
                # Vẽ điểm
                for pt in self.current_points:
                    cv2.circle(display_img, pt, 4, (0, 0, 255), -1)
                
                # Vẽ đường nối
                if len(self.current_points) > 1:
                    cv2.polylines(display_img, [np.array(self.current_points)], False, (0, 255, 0), 2)
            
            cv2.imshow(self.window_name, display_img)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('n'): # Next (Hoàn thành)
                if len(self.current_points) > 2: # Cần ít nhất 3 điểm để thành đa giác
                    self.done = True
                else:
                    print("Cần ít nhất 3 điểm!")
            elif key == ord('r'): # Reset
                self.current_points = []
                print("Đã xóa. Vẽ lại.")

        return self.current_points

    def close(self):
        cv2.destroyWindow(self.window_name)