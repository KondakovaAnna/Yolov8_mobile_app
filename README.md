mmcs course

To export model run this command:
yolo export model=./results/detect/yolov8n_custom/weights/best.pt format=tflite

Link to dataset:
https://app.roboflow.com/mmcscscourse/guitars-aqozo/1


To train model use command:
 docker run -v ./guitars:/training_data -v ./results:/runs  yolo_train task=detect mode=train model=yolov8n imgsz=640 data=/training_data/data.yaml epochs=2  batch=8 name=yolov8n_custom