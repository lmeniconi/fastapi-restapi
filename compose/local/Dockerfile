FROM python:3

WORKDIR /app

# Load dependencies and scripts
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY compose/local/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

CMD /start