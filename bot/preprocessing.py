from PIL import Image


class Preprocessor:
    def preprocess_image(self, image_path: str) -> Image:
        """Preprocess the image: convert to grayscale and increase contrast."""
        img = Image.open(image_path)
        img = img.convert("L")  # Convert to grayscale
        img = img.point(lambda x: 0 if x < 128 else 255)  # Increase contrast
        return img
