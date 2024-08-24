FROM python:3.9

MAINTAINER TalentC
WORKDIR /app
COPY requirements.txt .

ENV LANG C.UTF-8
RUN apt-get update
RUN apt-get install -y tzdata ca-certificates
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime

RUN pip install -r requirements.txt

COPY . .
CMD ["python", "-u", "main.py"]
