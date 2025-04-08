FROM python:3.12-slim

RUN apt update && apt install -y g++ libglib2.0-dev libpango1.0-dev

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["python", "app.py"]
