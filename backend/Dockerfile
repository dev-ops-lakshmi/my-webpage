FROM python:3.9-slim
RUN pip install flask flask-cors mysql-connector-python
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
