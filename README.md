# Telegram Automation Bot (Single Account)

⚠️ **HIGH RISK WARNING / هشدار جدی**

This project uses a **personal Telegram account** (userbot) to automatically:
- Send a message every **1 hour**
- Send another message every **2 hours**
- Join a list of groups **every day**

Telegram detects and restricts this kind of automation.  
**Your account can be limited or permanently banned.**  

Use only on a test/secondary account and **at your own risk**.  
The author accepts **no responsibility** for any bans or problems.

---

## What this bot does

### 1. Userbot (your personal account via Telethon)
- Hourly message to a target
- Message every 2 hours to the same target
- Daily attempt to join groups listed in config

### 2. Control Bot (official bot created with @BotFather)
- You send `/start`
- A button appears
- Pressing the button starts all three jobs

---

## Setup Guide

### Step 1: Get API_ID & API_HASH
1. Go to https://my.telegram.org
2. Log in with your phone number
3. Click **API development tools** and create an application
4. Copy `api_id` and `api_hash`

### Step 2: Create Control Bot
1. Open Telegram and talk to [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the steps
3. Copy the token (looks like `123456789:AA...`)

### Step 3: Get your numeric User ID
1. Talk to [@userinfobot](https://t.me/userinfobot)
2. Copy the number it gives you (this is `OWNER_CHAT_ID`)

### Step 4: Create config.py
```bash
cp config.example.py config.py
```
Open `config.py` and replace the example values with your real ones.

### Step 5: Install requirements
```bash
pip install -r requirements.txt
```

### Step 6: First run (login)
```bash
python bot.py
```
- Telegram will send you a login code → enter it in the terminal
- If you have 2FA, enter your password too
- A `.session` file will be created (keep it private!)

### Step 7: Start the automation
1. Open the control bot you created in Telegram
2. Send `/start`
3. Press the button «🚀 Start Automation»
4. You will receive confirmation that the jobs are running

---

## Running 24/7 on a VPS (recommended)

Because the bot must stay online, run it on a cheap VPS.

### Simple method with screen:
```bash
sudo apt update && sudo apt install screen -y
screen -S telegrambot
python3 bot.py
# Detach without stopping: Ctrl+A then D
```
Later return with: `screen -r telegrambot`

---

## Security Notes

- `config.py` and any `*.session` file are in `.gitignore` — never push them to GitHub.
- The `.session` file = full access to your Telegram account. Protect it.
- Keep `JOIN_DELAY_SECONDS` at 45 or higher.
- Start with only 1-2 groups and low frequency for testing.

---

## Disclaimer

This code is for educational and personal experimentation only.  
Automating personal accounts often violates Telegram Terms of Service.  
You are fully responsible for any consequences (account bans, restrictions, etc.).
