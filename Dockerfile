FROM python:3.11-slim

# Установим uv
RUN pip install uv

# Копируем проект
COPY . /app
WORKDIR /app

# Создаем виртуальную среду с uv
RUN uv venv venv

# Активируем виртуальную среду и устанавливаем зависимости
RUN . venv/bin/activate && uv pip install --no-cache-dir -r requirements.txt

# Открываем порт и запускаем Streamlit
EXPOSE 8501
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.enableCORS=false"]
