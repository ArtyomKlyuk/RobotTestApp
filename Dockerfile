# Используем базовый образ Python
FROM python:3.10

# Создаем и устанавливаем зависимости
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . /app/

# Устанавливаем переменную среды PYTHONUNBUFFERED для предотвращения буферизации вывода
ENV PYTHONUNBUFFERED 1

# Запускаем ваш скрипт при старте контейнера
CMD ["python", "-m", "server"]
