import logging
import os

from telegram import Update
from telegram.ext import CallbackContext

from .directory_manager import DirectoryManager

logger = logging.getLogger(__name__)


class ImageHandler:
    def __init__(self, image_dir):
        self.image_dir = image_dir
        self.dir_manager = DirectoryManager(image_dir)

    async def save_image(self, update: Update, context: CallbackContext) -> None:
        """Save received images to the specified directory."""
        photo = update.message.photo[-1]  # Get the largest size photo
        try:
            file = await photo.get_file()
            file_name = os.path.join(self.image_dir, f"{update.message.message_id}.jpg")

            self.dir_manager.ensure_directories()  # Ensure the directory exists
            await file.download_to_drive(file_name)
            await update.message.reply_text(
                "Image received. Send more or press 'Finish' when done."
            )
        except Exception as e:
            logger.error(f"Failed to handle image: {e}")
            await update.message.reply_text(
                "Failed to process the image. Please try again."
            )

    def get_image_files(self):
        """Retrieve a list of image files in the directory."""
        return [
            os.path.join(self.image_dir, f)
            for f in os.listdir(self.image_dir)
            if f.endswith(".jpg")
        ]
