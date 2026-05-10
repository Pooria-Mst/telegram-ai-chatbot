import requests
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters


# --- OLLAMA LOGIC (PASTE/REPLACE THIS PART) ---
def query_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    # Instructions to ensure it speaks the right language
    system_instruction = "You are a helpful assistant. Always reply in the same language the user uses."
    full_prompt = f"{system_instruction}\nUser: {prompt}"

    data = {
        "model": "llama3.2",
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=data, timeout=60)  # Added timeout for 3B model
        return response.json()['response']
    except Exception as e:
        return f"Error connecting to Ollama: {e}"


# --- UPDATE COMMAND ---
async def update_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Checking for AI updates... please wait.")
    try:
        process = subprocess.run(["ollama", "pull", "llama3.2"], capture_output=True, text=True)
        if process.returncode == 0:
            await update.message.reply_text("✅ My brain (Llama 3.2 3B) is up to date.")
        else:
            await update.message.reply_text("❌ Update failed.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")


# --- MESSAGE HANDLER ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    print(f"User: {user_text}")
    # Show "typing..." so the user waits during the 3B model's delay
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')

    ai_response = query_ollama(user_text)
    await update.message.reply_text(ai_response)


# --- RUN BOT ---
if __name__ == '__main__':
    # REMEMBER: Use your real token from BotFather here!
    application = ApplicationBuilder().token('YOUR_TOKEN_HERE').build()

    application.add_handler(CommandHandler("update", update_model))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot is running with Llama 3.2 (3B)...")
    application.run_polling()
