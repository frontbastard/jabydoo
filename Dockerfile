FROM python:3.10-alpine
WORKDIR /app
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
