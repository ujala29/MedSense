import cv2
import pytesseract
import numpy as np
from PIL import Image
import io


def preprocess_image(file_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(file_bytes))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray)
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    text = pytesseract.image_to_string(thresh)
    return text