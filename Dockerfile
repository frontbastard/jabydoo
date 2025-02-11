FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /staticfiles /media

RUN adduser --disabled-password --gecos "" app_user

RUN chown -R app_user:www-data /staticfiles /media
RUN chmod -R 755 /staticfiles /media
