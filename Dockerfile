FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["pytest", "--headless", "--executor=grid", "--grid-url=http://selenoid:4444/wd/hub", "-m", "ci"]
