import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Define directories
IMAGE_DIR = "images"
OUTPUT_DIR = "output"

# Define constants for languages
LANGUAGE_ENGLISH = "english"
LANGUAGE_RUSSIAN = "russian"

# Define callback data
FINISH_CALLBACK_DATA = "finish"

# Specify the path to the tesseract executable
TESSERACT_CMD = (
    r"X:\Program Files\Tesseract-OCR\tesseract.exe"  # Adjust path for Windows
)
