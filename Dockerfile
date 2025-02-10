FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN mkdir -p /app/staticfiles

RUN adduser --disabled-password --gecos "" app_user

RUN chown -R app_user:app_user /app/staticfiles
RUN chmod -R 755 /app/staticfiles
RUN python manage.py collectstatic --noinput
