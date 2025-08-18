import os
import requests
import cv2
import numpy as np
import json
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, List, Dict, Union  
from config import BASE_URL, COOKIES, CAMERAS, MAX_PREVIEW_WAIT_TIME, PREVIEW_CHECK_INTERVAL
from utils import hex_to_bgr, draw_regions

os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/camera_processor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def force_generate_new_preview(camera_uuid: str) -> Optional[str]:
    """Генерирует новое превью и возвращает его URL."""
    try:
        logger.info(f"Генерация превью для камеры {camera_uuid}...")
        generate_url = f"{BASE_URL}/api/cams/{camera_uuid}/stream-preview"
        response = requests.post(generate_url, cookies=COOKIES)
        response.raise_for_status()
        task_id = response.json()["data"]["id"]
        
        start_time = time.time()
        old_preview = get_camera_data(camera_uuid).get("previewUri", "")
        
        while time.time() - start_time < MAX_PREVIEW_WAIT_TIME:
            current_data = get_camera_data(camera_uuid)
            if current_data and current_data.get("previewUri", "") != old_preview:
                new_preview_url = f"{BASE_URL}{current_data['previewUri']}"
                logger.info(f"Новое превью: {new_preview_url}")
                return new_preview_url
            time.sleep(PREVIEW_CHECK_INTERVAL)
        
        logger.error(f"Таймаут ожидания превью для камеры {camera_uuid}")
        return None
    except Exception as e:
        logger.error(f"Ошибка генерации превью ({camera_uuid}): {str(e)}")
        return None

def get_camera_data(camera_uuid: str) -> Optional[Dict]:
    """Получаем данные камеры по UUID."""
    try:
        url = f"{BASE_URL}/api/cams/{camera_uuid}"
        response = requests.get(url, cookies=COOKIES)
        response.raise_for_status()
        return response.json()["data"]
    except Exception as e:
        logger.error(f"Ошибка получения данных камеры {camera_uuid}: {str(e)}")
        return None

def download_preview(preview_url: str) -> Optional[np.ndarray]:
    """Загружаем изображение превью."""
    try:
        response = requests.get(preview_url, cookies=COOKIES, stream=True)
        response.raise_for_status()
        img = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_COLOR)
        if img is not None:
            logger.info(f"Превью загружено. Размер: {img.shape[1]}x{img.shape[0]}")
            return img
        logger.error("Не удалось декодировать изображение")
        return None
    except Exception as e:
        logger.error(f"Ошибка загрузки превью: {str(e)}")
        return None

def get_regions(camera_uuid: str) -> List:
    """Получаем зоны камеры."""
    try:
        url = f"{BASE_URL}/api/cams/{camera_uuid}/regions"
        response = requests.get(url, cookies=COOKIES)
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as e:
        logger.error(f"Ошибка получения зон ({camera_uuid}): {str(e)}")
        return []

def save_image(image: np.ndarray, filename: str) -> bool:
    """Сохраняем изображение."""
    try:
        cv2.imwrite(filename, image)
        logger.info(f"Изображение сохранено: {filename}")
        return True
    except Exception as e:
        logger.error(f"Ошибка сохранения {filename}: {str(e)}")
        return False

def save_camera_changes(camera_uuid: str) -> bool:
    """Сохраняем изменения камеры на сервере."""
    try:
        cam_data = get_camera_data(camera_uuid)
        if not cam_data:
            return False

        url = f"{BASE_URL}/api/cams/{camera_uuid}"
        headers = {
            "X-CSRFToken": COOKIES["csrftoken"],
            "Referer": f"{BASE_URL}/cams/{camera_uuid}",
            "Content-Type": "application/json"
        }
        
        response = requests.patch(
            url,
            cookies=COOKIES,
            headers=headers,
            json=cam_data
        )
        response.raise_for_status()
        logger.info(f"Изменения камеры {camera_uuid} сохранены")
        return True
    except Exception as e:
        logger.error(f"Ошибка сохранения ({camera_uuid}): {str(e)}")
        return False

def process_camera(camera: Dict) -> bool:
    """Обрабатываем одну камеру."""
    camera_uuid = camera["uuid"]
    output_filename = camera["output_filename"]
    
    logger.info(f"\n{'='*50}\nОбработка камеры: {camera['name']} ({camera_uuid})")
    
    preview_url = force_generate_new_preview(camera_uuid)
    if not preview_url:
        return False
    
    preview = download_preview(preview_url)
    if preview is None:
        return False
    
    regions = get_regions(camera_uuid)
    result = draw_regions(preview, regions)
    
    if not save_image(result, output_filename):
        return False
    
    if not save_camera_changes(camera_uuid):
        return False
    
    return True

def main():
    """Запускает обработку всех камер."""
    logger.info("Старт обработки камер...")
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_camera, camera) for camera in CAMERAS]
        for future in futures:
            future.result()
    
    logger.info("Обработка завершена")

if __name__ == "__main__":
    main()