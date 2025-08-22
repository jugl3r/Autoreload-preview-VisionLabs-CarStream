# Автообновление превью и сохранение настроек камер VisionLabs Luna Cars

## 📌 Описание

Скрипт для автообновления превью с текущими зонами распознования и сохранения настроек камеры

## 📂 Структура репозитория

```plaintext
/Autoreload-preview-VisionLabs-CarStream
├── .env                # Переменные окружения
├── config.py           # Общие настройки
├── logs                # Директория для хранения логов
├── processor.py        # Основная логика
├── requirements.txt    # Необходимые зависимости
├── utils.py            # Вспомогательные функции
```

## 🚀 Установка и запуск

1. Клонирование репозитория:
   ```bash
   git clone git@github.com:jugl3r/Autoreload-preview-VisionLabs-CarStream.git
   cd Autoreload-preview-VisionLabs-CarStream
   ```
2. Создание виртуального окружения Python (рекомендуется):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Для Linux/macOS
   venv\Scripts\activate     # Для Windows
   ```
3. Установка зависимостей:
   ```bash
   pip3 install -r requirements.txt
   ```
4. Создание сессии с cookie:
   ```bash
   curl -X POST "http://<ip>:<port>/api/auth/login" \
   -H "Content-Type: application/json" \
   -d '{"login": "login", "password": "password"}' \
   --cookie-jar cookies.txt
   ```
5. Указать в `.env` файле URL страницы  VisionLabs и данные COOKIE из созданного файла "cookies.txt":
   ```bash
   BASE_URL=http://<ip>:<port>
   SESSION_ID=qwdysqwdtvt
   CSRF_TOKEN=asdsafgeag12
   ```

6. Указать настройки камер в 'config.py':
   ```bash
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
    ```
   Значение "uuid" можно взять по следующему пути:  
Зайти на фронт VisionLabs -> Камеры -> из поисковой строки взять uuid камеры 
(пример http://<ip>:<port>/cams/3dafba3a-e99f-4738-9fe4-129602719e6d из этой ссылки нам нужно "3dafba3a-e99f-4738-9fe4-129602719e6d" )

   Значения "name" и "output_filename" могут быть произвольными

6. Запуск в виртуальном окружении:
   ```bash
   python3 processor.py
   ```
p.s. на данный момент скрипт следует добавить в удобный для вас планировщик задач, что-бы он автоматически выполнял команду

