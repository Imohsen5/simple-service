import os

import pytesseract

from bot.preprocessing import Preprocessor
from config import IMAGE_DIR, TESSERACT_CMD


class OCRProcessor:
    def __init__(self, language: str):
        self.language = language
        self.lang_code = "eng" if language == "english" else "rus"
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
        self.preprocessor = Preprocessor()

    def process_images(self) -> list:
        """Process images and perform OCR."""
        image_files = [
            os.path.join(IMAGE_DIR, f)
            for f in os.listdir(IMAGE_DIR)
            if f.endswith(".jpg")
        ]

        if not image_files:
            raise FileNotFoundError("No images found in the directory.")

        texts = []
        for image_file in image_files:
            # Use Preprocessor to handle image preprocessing
            preprocessed_img = self.preprocessor.preprocess_image(image_file)
            text = pytesseract.image_to_string(preprocessed_img, lang=self.lang_code)
            texts.append(text)

        return texts
