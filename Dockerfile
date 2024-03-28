# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости и файлы проекта в рабочую директорию контейнера
COPY requirements.txt ./
COPY bot.py ./
COPY .env ./

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir -r req.txt

# Команда для запуска бота
CMD [ "python", "bot.py" ]
