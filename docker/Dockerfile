FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY store/ /app
COPY docker/entrypoint.sh /app
RUN  ./manage.py makemigrations
RUN chmod 777 entrypoint.sh
RUN apt-get update && apt-get install -y netcat-openbsd


EXPOSE 8000
CMD ["./entrypoint.sh"]
