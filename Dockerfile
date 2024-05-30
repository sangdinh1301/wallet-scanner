FROM python:3.10.6

COPY . /var/www/app

WORKDIR /var/www/app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
