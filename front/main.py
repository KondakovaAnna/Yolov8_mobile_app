import streamlit as st
from io import StringIO
import requests
import os
from PIL import Image
from io import BytesIO
import cv2

BENTO_HOST = os.getenv("BENTO_HOST", "localhost")
BENTO_PORT = os.getenv("BENTO_PORT", "3000")

def highlight_borders(img: str, info: dict):
    boxes = [x["box"] for x in info] 
    probs = [x["confidence"] for x in info]
    cls = [x["class"] for x in info] 
    names = [x["name"] for x in info]

    image = cv2.imread(img, cv2.IMREAD_COLOR)

    detection_visualization = image.copy()

    text_font = cv2.FONT_HERSHEY_DUPLEX
    text_scale = 2.0
    colors = [(50, 20, 200), (200, 20, 100)]
    text_thickness = 5

    for detecion_id in range(len(boxes)):
        target_object_name = names[detecion_id]
        tob = boxes[detecion_id]  # XYXY format
        target_object_prob = float(probs[detecion_id])

        detection_visualization = cv2.rectangle(
          detection_visualization,
            tuple([int(tob["x1"]), int(tob["y1"])]),
            tuple([int(tob["x2"]), int(tob["y2"])]),
            colors[detecion_id % len(colors)],
            5
        )
    
    for detecion_id in range(len(boxes)):
        target_object_name = names[detecion_id]
        tob = boxes[detecion_id]
        target_object_prob = float(probs[detecion_id])

        input_text = '{} {:.2f}'.format(target_object_name, target_object_prob)

        (text_width, text_height), baseline = cv2.getTextSize(input_text, text_font, text_scale, text_thickness)

        detection_visualization = cv2.putText(
            detection_visualization,
            input_text,
            (int(tob["x1"]) + 10, int(tob["y1"]) + text_height + baseline),
            text_font,
            text_scale,
            colors[detecion_id % len(colors)],
            text_thickness
        )
    
    cv2.imwrite(f"gen_{img}", detection_visualization)




def post_img(route: str,img):
    r = requests.post(
        url=f"http://{BENTO_HOST}:{BENTO_PORT}{route}",
        files={"images": img}
    )

    if r.status_code not in [200,201]:
        raise Exception("blyat")
    return r

uploaded_file = st.file_uploader("Choose a file", type=["png","jpg","jpeg"])
if uploaded_file is not None:
    with open(uploaded_file.name,"wb") as f: 
        f.write(uploaded_file.getbuffer())         
    result = post_img("/predict", open(uploaded_file.name, 'rb'))
    #st.write(result.json())
    highlight_borders(uploaded_file.name, result.json())
    st.image(Image.open(f"gen_{uploaded_file.name}"))
    #st.image(uploaded_file)
