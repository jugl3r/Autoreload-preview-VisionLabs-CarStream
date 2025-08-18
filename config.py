import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
COOKIES = {
    "sessionid": os.getenv("SESSION_ID"),
    "csrftoken": os.getenv("CSRF_TOKEN")
}

CAMERAS = [
    {
        "uuid": "3dafba3a-e99f-4738-9fe4-129602719e6d",
        "name": "Enter",
        "output_filename": "camera_enter_1.jpg"
    },
    {
        "uuid": "d9991689-2e0b-49f2-b854-9943e6c30be2",
        "name": "Exit",
        "output_filename": "camera_exit_2.jpg"
    }
]

# Параметры для отрисовки зон
ALPHA = 0.4
CONTOUR_THICKNESS = 3
FONT_SCALE = 0.7
FONT_THICKNESS = 2
MAX_PREVIEW_WAIT_TIME = 10
PREVIEW_CHECK_INTERVAL = 1