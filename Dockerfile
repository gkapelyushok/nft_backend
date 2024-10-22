# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Открываем порт для Django
EXPOSE 8000

# Команда для запуска сервиса
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
