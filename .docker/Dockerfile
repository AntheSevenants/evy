FROM python:3.10-slim

WORKDIR /usr/app/src

# For production, we copy source code to /usr/app/src
COPY . /usr/app/src/

# Then, copy the requirements manually
COPY requirements.txt .
RUN pip install -r requirements.txt

CMD [ "python", "-u", "./server.py"]