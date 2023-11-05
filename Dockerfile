FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY recruitment /app/recruitment

RUN pip install -r requirements.txt

WORKDIR /app/recruitment

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
