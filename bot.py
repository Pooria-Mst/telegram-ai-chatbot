"""
Local AI Telegram Chatbot
=========================
A privacy-first Telegram chatbot powered by Ollama running Llama 3.2 (3B) locally.
All inference happens on your machine — no data sent to external AI providers.

Author : Pooria Mostafapoor
GitHub : https://github.com/pooriamostafapoor
"""

import os
import requests
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters


# ── CONFIGURATION ────────────────────────────────────────────────

OLLAMA_URL   = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"

# Load token from environment variable (never hardcode your token)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN environment variable is not set.\n"
        "Create a .env file or set the variable in your terminal:\n"
        "  Windows: set TELEGRAM_BOT_TOKEN=your_token_here\n"
        "  Mac/Linux: export TELEGRAM_BOT_TOKEN=your_token_here"
    )


# ── OLLAMA INFERENCE ─────────────────────────────────────────────

def query_ollama(user_message: str) -> str:
    """
    Send a user message to the locally running Ollama instance
    and return the AI-generated response.

    The system instruction ensures the model always replies in the
    same language the user writes in (multilingual support).

    Args:
        user_message: The raw text message from the Telegram user.

    Returns:
        The model's response as a string, or an error message if
        the Ollama server is unreachable.
    """
    system_instruction = (
        "You are a helpful assistant. "
        "Always reply in the same language the user uses."
    )
    full_prompt = f"{system_instruction}\nUser: {user_message}"

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        return response.json().get("response", "I could not generate a response.")
    except requests.exceptions.ConnectionError:
        return (
            "⚠️ Cannot connect to Ollama. "
            "Please make sure Ollama is running: open a terminal and run `ollama serve`."
        )
    except requests.exceptions.Timeout:
        return "⏱️ The model took too long to respond. Please try again."
    except Exception as e:
        return f"⚠️ Unexpected error: {e}"


# ── COMMAND HANDLERS ─────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /start command.
    Sends a welcome message explaining how to use the bot.
    """
    welcome = (
        "👋 Hello! I'm your local AI assistant powered by Llama 3.2.\n\n"
        "I run entirely on this machine — your conversations are private "
        "and never sent to any external AI service.\n\n"
        "Just send me any message and I'll reply!\n\n"
        "📌 Commands:\n"
        "  /start  — Show this welcome message\n"
        "  /update — Update the AI model to the latest version"
    )
    await update.message.reply_text(welcome)


async def update_model(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /update command.
    Uses subprocess to run `ollama pull` and update the model remotely,
    without needing to touch the terminal manually.
    """
    await update.message.reply_text(
        f"🔄 Checking for updates to {OLLAMA_MODEL}... please wait."
    )

    try:
        process = subprocess.run(
            ["ollama", "pull", OLLAMA_MODEL],
            capture_output=True,
            text=True,
            timeout=300   # 5-minute timeout for large model downloads
        )

        if process.returncode == 0:
            await update.message.reply_text(
                f"✅ {OLLAMA_MODEL} is up to date and ready."
            )
        else:
            await update.message.reply_text(
                f"❌ Update failed.\n\nDetails:\n{process.stderr}"
            )

    except FileNotFoundError:
        await update.message.reply_text(
            "⚠️ Ollama is not installed or not found in PATH."
        )
    except subprocess.TimeoutExpired:
        await update.message.reply_text(
            "⏱️ Update timed out. Please try again or run `ollama pull` manually."
        )
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error during update: {e}")


# ── MESSAGE HANDLER ───────────────────────────────────────────────

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle all incoming text messages.

    Workflow:
    1. Show a "typing..." indicator so the user knows the bot is working.
    2. Forward the message to the local Ollama inference server.
    3. Send the AI response back to the user on Telegram.

    Uses async/await so the bot can handle multiple users concurrently
    without blocking while waiting for the model to respond.
    """
    user_text = update.message.text
    print(f"[{update.effective_user.first_name}]: {user_text}")

    # Show typing indicator — important UX for slower 3B model responses
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    ai_response = query_ollama(user_text)
    await update.message.reply_text(ai_response)
    print(f"[Bot]: {ai_response[:80]}...")


# ── ENTRY POINT ───────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"🤖 Starting bot with {OLLAMA_MODEL}...")
    print(f"   Ollama endpoint: {OLLAMA_URL}")
    print(f"   Press Ctrl+C to stop.\n")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start",  start))
    app.add_handler(CommandHandler("update", update_model))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running. Open Telegram and send a message!\n")
    app.run_polling()
