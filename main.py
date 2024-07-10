# main.py

import logging

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from bot.handlers import BotHandlers
from config import TELEGRAM_TOKEN

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    # Initialize the Application with the bot token
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Create an instance of BotHandlers
    bot_handlers = BotHandlers(application)

    # Register handlers
    application.add_handler(CommandHandler("start", bot_handlers.start))
    application.add_handler(
        CallbackQueryHandler(bot_handlers.handle_language_selection)
    )
    application.add_handler(MessageHandler(filters.PHOTO, bot_handlers.handle_image))
    application.add_handler(CommandHandler("finish", bot_handlers.handle_finish))

    # Start the bot
    logger.info("Starting the bot...")
    application.run_polling()


if __name__ == "__main__":
    main()
