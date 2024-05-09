FROM python:3.10

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

WORKDIR /app/bot

HEALTHCHECK CMD discordhealthcheck || exit 1

CMD ["python3", "main.py"]