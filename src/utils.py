import cv2
import numpy as np

def draw_text(img, text, pos, color=(255, 255, 255), scale=0.8, thickness=2):
    """
    Vẽ text lên ảnh với viền đen để dễ đọc.
    """
    x, y = pos
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 0, 0), thickness + 2)
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness)

def is_point_in_polygon(point, polygon):
    """
    Kiểm tra một điểm có nằm trong đa giác hay không.
    point: (x, y)
    polygon: list of points [(x1, y1), (x2, y2), ...]
    """
    pts = np.array(polygon, np.int32)
    pts = pts.reshape((-1, 1, 2))
    # result > 0: inside, < 0: outside, = 0: on edge
    result = cv2.pointPolygonTest(pts, point, False)
    return result >= 0

def draw_polygon(img, polygon, color=(0, 255, 0), thickness=2, label=None):
    """
    Vẽ đa giác lên ảnh.
    """
    pts = np.array(polygon, np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(img, [pts], True, color, thickness)
    
    if label:
        # Tìm điểm trên cùng bên trái để vẽ label
        x, y = polygon[0]
        draw_text(img, label, (x, y - 10), color=color)
