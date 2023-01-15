FROM python:3.10
COPY . /chain
WORKDIR /chain
RUN pip3 install -r requirements.txt -i "http://mirrors.aliyun.com/pypi/simple" --trusted-host "mirrors.aliyun.com"
EXPOSE 5000
CMD uwsgi --ini uwsgi.ini