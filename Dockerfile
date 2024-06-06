FROM python:3.10-slim
LABEL authors="Aleksandar Filipovic"

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--port", "8000"]