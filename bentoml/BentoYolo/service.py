from __future__ import annotations

import logging

import joblib
import tensorflow as tf

import json
import os
import typing as t
from typing import BinaryIO
from pathlib import Path
import PIL
from PIL.Image import Image as PILImage
import bentoml
from bentoml.validators import ContentType
from pydantic import BaseModel
import numpy as np

"""
class Params(BaseModel):
    images: PILImage
    arbitrary_types_allowed=True
"""

Image = t.Annotated[Path, ContentType("image/*")]


@bentoml.service(resources={"gpu": 1})
class YoloV8:
    def __init__(self):
        from ultralytics import YOLO

        yolo_model = os.getenv("YOLO_MODEL", "./best.pt")

        self.model = YOLO(yolo_model)

    @bentoml.api()
    def predict(self, images: PILImage) -> list[dict]:
        print(images)
        results = self.model.predict(images)[0]
        return json.loads(results.tojson())
        #return [json.loads(result.tojson()) for result in results]

    @bentoml.api
    def render(self, images: PILImage) -> PILImage:
        result = self.model.predict(images)[0]
        output = "aaaaaa.jpeg" #images.parent.joinpath(f"{images.stem}_result{images.suffix}")
        result.save(output)
        return Image.open(output)
