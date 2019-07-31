FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
CMD [ "python", "./main.py" ]