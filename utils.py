import cv2
import numpy as np
import logging
from config import ALPHA, CONTOUR_THICKNESS, FONT_SCALE, FONT_THICKNESS

def hex_to_bgr(hex_color: str) -> tuple:
    """Конвертируем HEX цвет в BGR."""
    hex_color = hex_color.lstrip('#')
    r, g, b = [min(255, int(hex_color[i:i+2], 16) + 40) for i in (0, 2, 4)]
    return (b, g, r)

def draw_regions(image: np.ndarray, regions: list) -> np.ndarray:
    """Рисуем зоны на изображении."""
    if not regions:
        logging.warning("Нет зон для отрисовки")
        return image
        
    overlay = image.copy()
    output = image.copy()
    
    for region in regions:
        try:
            points = np.array([[p['x'], p['y']] for p in region['points']], dtype=np.int32)
            color = hex_to_bgr(region['displayColor'])
            
            cv2.fillPoly(overlay, [points], color)
            cv2.polylines(output, [points], True, color, CONTOUR_THICKNESS)
            
            text = region['tagName']
            text_pos = (points[0][0], points[0][1] - 10)
            cv2.putText(output, text, text_pos, 
                       cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, 
                       (255, 255, 255), FONT_THICKNESS)
        except Exception as e:
            logging.error(f"Ошибка отрисовки зоны: {str(e)}")
    
    cv2.addWeighted(overlay, ALPHA, output, 1 - ALPHA, 0, output)
    return output