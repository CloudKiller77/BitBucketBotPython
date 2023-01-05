FROM python:3.10

WORKDIR /home

# ENV TELEGRAM_API_TOKEN=""
# ENV TELEGRAM_ACCESS_ID=""
# ENV TELEGRAM_PROXY_URL=""
# ENV TELEGRAM_PROXY_LOGIN=""
# ENV TELEGRAM_PROXY_PASSWORD=""

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && pip install -r /requirements.txt
# RUN pip install -U pip aiogram pytz && apt-get update && apt-get install sqlite3
COPY *.py ./

ENTRYPOINT ["python", "main.py"]
