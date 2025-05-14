FROM ubuntu:24.04

RUN apt-get update && apt-get install -y python3 python3-pip sudo xvfb wget

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

COPY main.py /app

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "8", "--timeout", "900", "--graceful-timeout", "600", "main:app"]