# 🤖 Local AI Telegram Chatbot

A **privacy-first, locally-hosted AI chatbot** built with Python and Telegram Bot API, powered by [Ollama](https://ollama.com/) running **Llama 3.2 (3B)** entirely on your own machine — no third-party cloud AI, no data leaving your device.

---

## ✨ Features

- 🔒 **Fully Local Inference** — All AI processing runs on your hardware via Ollama. No OpenAI, no Anthropic, no data sent to external AI providers.
- 🌐 **Multilingual** — Automatically replies in the same language the user writes in, powered by a custom system prompt.
- ⚡ **Async Message Handling** — Built with `asyncio` for responsive, non-blocking message processing even under concurrent users.
- ⌨️ **Typing Indicator** — Shows a real-time "typing..." status while the model is thinking, so users always know the bot is working.
- 🔄 **Remote Model Updates** — The `/update` command lets you pull the latest version of the AI model directly from Telegram — no terminal needed.
- 🛠️ **Subprocess Automation** — Uses Python's `subprocess` module to interface with the Ollama CLI for system-level model management.

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Bot Framework | `python-telegram-bot` v20+ |
| LLM Runtime | Ollama |
| AI Model | Llama 3.2 (3B) |
| Async | `asyncio` |
| HTTP Client | `requests` |
| Automation | `subprocess` |
| Environment | Windows Terminal / PowerShell |

---

## 🏗️ Architecture

```
User (Telegram App)
        │
        ▼
Telegram Cloud Servers
        │  (HTTPS polling)
        ▼
┌─────────────────────────────┐
│        bot.py               │
│  ┌─────────────────────┐    │
│  │  MessageHandler     │    │
│  │  (async/await)      │    │
│  └────────┬────────────┘    │
│           │                 │
│  ┌────────▼────────────┐    │
│  │  query_ollama()     │    │
│  │  HTTP POST →        │    │
│  │  localhost:11434    │    │
│  └────────┬────────────┘    │
└──────────────────────────── ┘
           │
           ▼
┌─────────────────────────────┐
│   Ollama (Local Server)     │
│   Model: Llama 3.2 (3B)     │
│   Runs 100% on your machine │
└─────────────────────────────┘
```

---

## 📋 Prerequisites

Before you begin, make sure you have:

- Python 3.10 or higher
- [Ollama](https://ollama.com/download) installed and running
- Llama 3.2 model pulled (`ollama pull llama3.2`)
- A Telegram bot token from [@BotFather](https://t.me/botfather)

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/telegram-ai-chatbot.git
cd telegram-ai-chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Pull the AI model

Make sure Ollama is running, then pull the model:

```bash
ollama pull llama3.2
```

### 4. Configure your bot token

Copy the example environment file and add your token:

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder:

```
TELEGRAM_BOT_TOKEN=your_real_token_from_botfather_here
```

> ⚠️ **Never commit your `.env` file or paste your token directly into the code.** The `.gitignore` in this repo already excludes `.env`.

### 5. Run the bot

```bash
python bot.py
```

You should see:
```
Bot is running with Llama 3.2 (3B)...
```

---

## 💬 Usage

Once the bot is running, open Telegram and send a message to your bot.

| Action | Command / Input |
|---|---|
| Chat with AI | Send any text message |
| Update the AI model | `/update` |

### Example interaction

```
You:  What is machine learning?
Bot:  Machine learning is a subset of artificial intelligence where systems
      learn from data to improve their performance over time without being
      explicitly programmed...

You:  ما هو تعلم الآلة؟
Bot:  تعلم الآلة هو فرع من فروع الذكاء الاصطناعي...
```

---

## ⚙️ How It Works

### Message Flow
1. User sends a message on Telegram
2. Telegram's servers forward it to your bot via HTTPS polling
3. `handle_message()` receives it asynchronously and sends a typing indicator
4. `query_ollama()` sends the message to Ollama's local REST API (`localhost:11434`)
5. Ollama runs inference with Llama 3.2 on your machine
6. The response is returned and sent back to the user on Telegram

### Multilingual System Prompt
A system instruction is prepended to every query:
```python
system_instruction = "You are a helpful assistant. Always reply in the same language the user uses."
```
This ensures the model responds in Persian, Arabic, Spanish, or any other language the user writes in — without any extra configuration.

### Remote Model Update
The `/update` command runs:
```python
subprocess.run(["ollama", "pull", "llama3.2"])
```
This lets you update the AI model remotely through Telegram without touching your terminal.

---

## 🗂️ Project Structure

```
telegram-ai-chatbot/
│
├── bot.py               # Main bot logic
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── .gitignore           # Files excluded from Git
└── README.md            # This file
```

---

## 🔮 Future Improvements

- [ ] Add conversation memory (multi-turn context)
- [ ] Support model switching via bot commands (e.g. `/model mistral`)
- [ ] Add `/help` command listing all available features
- [ ] Deploy on a local server or Raspberry Pi for 24/7 uptime
- [ ] Add user authentication to restrict bot access
- [ ] Stream responses token-by-token for faster perceived response time
- [ ] Integrate with LangChain for tool use and agent capabilities

---

## 🙋 Author

**Pooria Mostafapoor**
- [LinkedIn](https://www.linkedin.com/in/pooriamostafapoor)
- [Kaggle](https://www.kaggle.com/pooriamostafapoor)
- [GitHub](https://github.com/pooriamostafapoor)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
