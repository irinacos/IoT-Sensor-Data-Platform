FROM python:3.10
WORKDIR /app
COPY adapter.py ./
COPY requirements.txt ./
RUN apt-get update && apt-get install -y mosquitto-clients
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "adapter.py"]