import os
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
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

# Define a simple /help command as mentioned in your message
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("How can I help you? You can use the menu or contact support.")

# Dummy HTTP Server to satisfy Render's port binding requirement
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_health_check_server():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    print(b"Health check server started on port", port)
    server.serve_forever()

def main():
    # Get token from environment variables (set this up on Render)
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    
    if not TOKEN:
        print("Error: No TELEGRAM_TOKEN found in environment variables.")
        return

    # Start the dummy health check server in a background thread
    threading.Thread(target=run_health_check_server, daemon=True).start()

    # Build the Telegram Bot application
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot using polling
    print("Bot is polling...")
    application.run_polling()

if __name__ == "__main__":
    main()
