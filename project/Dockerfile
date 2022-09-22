FROM python:3.8
LABEL maintainer="Richard Irving"

WORKDIR /app
COPY ./techtrends/requirements.txt ./

RUN pip install -r requirements.txt

COPY ./techtrends ./

RUN python init_db.py

COPY ./techtrends/database.db ./

EXPOSE 3111

CMD [ "python", "app.py" ]
