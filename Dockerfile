FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/staticfiles /app/media

RUN adduser --disabled-password --gecos "" app_user

RUN chown -R app_user:app_user /app/staticfiles /app/media
RUN chmod -R 755 /app/staticfiles /app/media

USER app_user
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "unix:/app/app.sock", "site_service.wsgi:application", "--workers", "3"]
