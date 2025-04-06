FROM python:3.11-slim

# Установим uv
RUN pip install uv

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN uv pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . /app
WORKDIR /app

# Открываем порт и запускаем Streamlit
EXPOSE 8501
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.enableCORS=false"]
