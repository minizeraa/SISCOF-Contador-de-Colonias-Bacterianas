import base64
import io
import math

import numpy as np
from PIL import Image


class Circulo:
    def __init__(self, y: int, x: int, raio: int):
        self.x = x
        self.y = y
        self.raio = raio

    def get_distance(self, point: tuple[int, int]) -> float:
        return abs(math.dist([self.x, self.y], point))

    def get_croped_img_out(self, img) -> np.ndarray:
        return img[
            round(self.y - self.raio*1.2):round(self.y + self.raio*1.2),
            round(self.x - self.raio*1.2):round(self.x + self.raio*1.2)
        ]

    def get_croped_img_in(self, img, coef=math.sqrt(2)/2) -> np.ndarray:
        return img[
            round(self.y - self.raio*coef):round(self.y + self.raio*coef),
            round(self.x - self.raio*coef):round(self.x + self.raio*coef)
        ]

    def get_data_img(self, img) -> str:  # SystemError
        croped = self.get_croped_img_out(img)

        with io.BytesIO() as buffer:
            Image.fromarray(croped).save(buffer, format='png')
            data = base64.encodebytes(buffer.getvalue()).decode("utf-8")

        buffer = f"data:image/png;base64,{data}"

        return buffer

    def get_median_color(self, img) -> float:
        croped = self.get_croped_img_in(img)
        return float(np.median(croped))

    def get_darker_median_color(self, img, porcentual=2) -> float:
        pixels = img.flatten()
        pixels_ordenados = np.sort(pixels)
        limite = int(len(pixels_ordenados) * (porcentual / 100))
        pixels_mais_escuros = pixels_ordenados[:limite]
        media_pixels_mais_escuros = float(np.mean(pixels_mais_escuros))

        return media_pixels_mais_escuros

    def __repr__(self):
        return f"Circulo({self.x}, {self.y}, {self.raio})"

class Colonia(Circulo):
    pass