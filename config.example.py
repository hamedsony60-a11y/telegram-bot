# =========================================
# Configuration example
# Copy this file to config.py and fill real values
# NEVER upload config.py or *.session to GitHub!
# =========================================

# --- Userbot (personal account) ---
# Get from https://my.telegram.org
API_ID = 1234567
API_HASH = "your_api_hash_here"

# Phone with country code (example: +989123456789)
PHONE = "+98XXXXXXXXXX"

SESSION_NAME = "my_session"

# Where to send the messages (username or numeric ID)
TARGET = "@your_target_username"

MESSAGE_HOURLY = "This message is sent every 1 hour."
MESSAGE_EVERY_2H = "This message is sent every 2 hours."

GROUP_LINKS = [
    "https://t.me/group1",
    "https://t.me/group2",
    "https://t.me/group3",
    "https://t.me/group4",
    "https://t.me/group5",
    "https://t.me/group6",
    "https://t.me/group7",
]

# Delay between each join (seconds). Keep high to reduce ban risk.
JOIN_DELAY_SECONDS = 45

# --- Control Bot (from @BotFather) ---
CONTROL_BOT_TOKEN = "123456789:AAExampleTokenHere"

# Your numeric Telegram user ID (from @userinfobot)
# Only this ID can press the start button
OWNER_CHAT_ID = 123456789
