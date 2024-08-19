FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN pip install Flask-SQLAlchemy
RUN pip install flask-jwt-extended
RUN pip install flask-apscheduler
RUN pip install --upgrade Flask Flask-Bcrypt bcrypt

COPY . .

EXPOSE 5000

CMD ["python", "run.py"]
