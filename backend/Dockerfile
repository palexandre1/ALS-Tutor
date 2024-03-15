FROM amd64/python:3.10.9-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow_cpu-2.15.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

RUN pip install -r requirements.txt

EXPOSE 8080

CMD [ "flask", "run","--host","0.0.0.0","--port","8080"]