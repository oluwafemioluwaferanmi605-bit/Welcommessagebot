import os
import asyncio
from aiohttp import web
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# The welcome message you requested
WELCOME_TEXT = """
Welcome to Welcommessagebot

We're excited to have you here. 

This bot is designed to help you with:
Fast support
Easy navigation
Instant updates
Helpful tools & resources

Use the menu below or type /help to get started.

Need assistance? Our team is always here for you.

Enjoy your experience with us.
"""

# Define the /start command behavior
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(WELCOME_TEXT)

# Define a simple /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("How can I help you? You can use the menu or contact support.")

# Asynchronous health check handler for Render
async def handle_health_check(request):
    return web.Response(text="Bot is running!")

async def main():
    # Get token from environment variables
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TOKEN:
        print("Error: No TELEGRAM_TOKEN found in environment variables.")
        return

    # Build the Telegram Bot application
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Set up the web server for Render's health check
    app = web.Application()
    app.router.add_get('/', handle_health_check)
    
    port = int(os.environ.get("PORT", 8000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    
    # Start the web server
    await site.start()
    print(f"Health check server started on port {port}")

    # Initialize and start the telegram bot polling inside the same async event loop
    await application.initialize()
    await application.start()
    print("Bot is polling...")
    await application.updater.start_polling()

    # Keep running until interrupted
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        # Clean up nicely on shutdown
        await application.updater.stop()
        await application.stop()
        await application.shutdown()
        await runner.cleanup()

if __name__ == "__main__":
    # Explicitly run using the modern asyncio entry point
    asyncio.run(main())
