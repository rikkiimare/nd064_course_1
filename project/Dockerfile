FROM python:3.8
LABEL maintainer="Richard Irving"

WORKDIR /app
COPY ./techtrends ./

RUN pip install -r requirements.txt

EXPOSE 3111

RUN python init_db.py
CMD [ "python", "app.py" ]
