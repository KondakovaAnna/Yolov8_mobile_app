FROM ubuntu:20.04

COPY requirements.txt .

RUN apt-get update && \
    apt-get install ffmpeg libsm6 libxext6  -y && \
    apt-get install --no-install-recommends -y curl screen python3 build-essential python3-pip

RUN python3 -m pip install -r requirements.txt
CMD yolo task=detect mode=train model=yolov8n imgsz=640 data=/training_data/data.yaml epochs=1  batch=8 name=yolov8n_custom
