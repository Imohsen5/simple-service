import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from config import IMAGE_DIR, LANGUAGE_ENGLISH, LANGUAGE_RUSSIAN, OUTPUT_DIR
from ocr_processor import OCRProcessor

from .directory_manager import DirectoryManager
from .image_handler import ImageHandler
from .pdf_maker import PDFMaker
from .preprocessing import Preprocessor

logger = logging.getLogger(__name__)


class BotHandlers:
    def __init__(self, application):
        self.application = application
        self.dir_manager = DirectoryManager(IMAGE_DIR, OUTPUT_DIR)
        self.image_handler = ImageHandler(IMAGE_DIR)
        self.pdf_maker = PDFMaker()
        self.preprocessor = Preprocessor()
        self.ocr_processor = OCRProcessor

        # Ensure directories exist
        self.dir_manager.ensure_directories()

    async def start(self, update: Update, context: CallbackContext) -> None:
        """Send a message asking the user for the language of the document."""
        keyboard = [
            [InlineKeyboardButton("English", callback_data=LANGUAGE_ENGLISH)],
            [InlineKeyboardButton("Russian", callback_data=LANGUAGE_RUSSIAN)],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Please select the language of the document:", reply_markup=reply_markup
        )

    async def handle_language_selection(
        self, update: Update, context: CallbackContext
    ) -> None:
        """Handle the user's language selection and ask for images."""
        query = update.callback_query
        language = query.data
        context.user_data["language"] = language
        await query.answer()
        await query.message.reply_text(
            "Please send me the images. After sending all images, press the 'Finish' button."
        )

    async def handle_image(self, update: Update, context: CallbackContext) -> None:
        """Handle received images and save them."""
        await self.image_handler.save_image(update, context)

    async def handle_finish(self, update: Update, context: CallbackContext) -> None:
        """Process images and perform OCR, then send the results to the user."""
        language = context.user_data.get("language", LANGUAGE_ENGLISH)
        ocr_processor = self.ocr_processor(language)

        # Ensure directories exist
        self.dir_manager.ensure_directories()

        # Debugging: Log directory contents
        image_files = self.image_handler.get_image_files()
        logger.info(f"Found images: {image_files}")

        try:
            # Process images and extract texts
            texts = ocr_processor.process_images()
            # Create the PDF from texts
            pdf_path = os.path.join(OUTPUT_DIR, "result.pdf")
            self.pdf_maker.create_pdf(texts, pdf_path)
        except FileNotFoundError:
            await update.message.reply_text(
                "No images found. Please send images before pressing 'Finish'."
            )
            return
        except Exception as e:
            logger.error(f"Failed to process images: {e}")
            await update.message.reply_text(
                "Failed to process images. Please try again."
            )
            return

        # Send text messages to the user
        for text in texts:
            await update.message.reply_text(
                text[:4096]
            )  # Telegram has a limit of 4096 characters per message

        # Send PDF to the user
        try:
            await self.pdf_maker.send_pdf(update, pdf_path)
        except Exception as e:
            logger.error(f"Failed to send PDF: {e}")
            await update.message.reply_text(
                "Failed to send the document. Please try again."
            )

        # Cleanup
        self.dir_manager.cleanup()
