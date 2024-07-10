import logging

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

logger = logging.getLogger(__name__)


class PDFMaker:
    def __init__(self):
        pass

    def create_pdf(self, text_list, output_path):
        """Create a PDF from the provided list of text strings."""
        try:
            c = canvas.Canvas(output_path, pagesize=letter)
            width, height = letter
            margin = 0.5 * inch
            current_y = height - margin

            for text in text_list:
                lines = text.split("\n")
                for line in lines:
                    if current_y < margin:
                        c.showPage()  # Create a new page
                        current_y = height - margin
                    c.drawString(margin, current_y, line)
                    current_y -= 12  # Move to the next line

            c.save()
            logger.info(f"PDF created successfully: {output_path}")
        except Exception as e:
            logger.error(f"Failed to create PDF: {e}")
            raise

    async def send_pdf(self, update, pdf_path):
        """Send the generated PDF to the user."""
        try:
            with open(pdf_path, "rb") as f:
                await update.message.reply_document(f)
            logger.info(f"PDF sent successfully: {pdf_path}")
        except Exception as e:
            logger.error(f"Failed to send PDF: {e}")
            raise
