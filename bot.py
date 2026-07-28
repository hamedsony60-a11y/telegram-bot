"""
Telegram Automation Script (Single Account + Control Button)
----------------------------------------------------------
⚠️  WARNING / هشدار مهم:
Using a personal Telegram account (userbot) for automated messaging
and automatic group joining has a HIGH RISK of account restriction
or permanent ban by Telegram.

Use only on a secondary/test account and at your own risk.
Keep join delays high. The author accepts no responsibility.
"""

import asyncio
import logging

from telethon import TelegramClient
from telethon.errors import (
    UserAlreadyParticipantError,
    FloodWaitError,
    InviteHashExpiredError,
    ChannelsTooMuchError,
)
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

client = TelegramClient(config.SESSION_NAME, config.API_ID, config.API_HASH)
scheduler = AsyncIOScheduler()
jobs_started = False


async def send_message(text: str):
    """Send a text message to the target defined in config.py"""
    try:
        await client.send_message(config.TARGET, text)
        log.info(f"Message sent: {text[:50]}")
    except FloodWaitError as e:
        log.warning(f"FloodWait: sleeping {e.seconds} seconds")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        log.error(f"Error sending message: {e}")


async def join_single_group(link: str):
    """Join one group/channel by invite link or username"""
    try:
        if "joinchat" in link or "/+" in link:
            invite_hash = link.rstrip("/").split("/")[-1].lstrip("+")
            await client(ImportChatInviteRequest(invite_hash))
        else:
            username = link.rstrip("/").split("/")[-1]
            await client(JoinChannelRequest(username))
        log.info(f"Successfully joined: {link}")

    except UserAlreadyParticipantError:
        log.info(f"Already a member: {link}")

    except InviteHashExpiredError:
        log.error(f"Invite link expired/invalid: {link}")

    except ChannelsTooMuchError:
        log.error("Too many channels/groups joined (Telegram limit).")

    except FloodWaitError as e:
        log.warning(f"FloodWait on join: sleeping {e.seconds} seconds")
        await asyncio.sleep(e.seconds)

    except Exception as e:
        log.error(f"Error joining {link}: {e}")


async def join_groups():
    """Try to join all groups listed in config.py"""
    log.info("Starting daily group join process...")
    for link in config.GROUP_LINKS:
        await join_single_group(link)
        await asyncio.sleep(config.JOIN_DELAY_SECONDS)
    log.info("Daily join process finished.")


def start_automation_jobs() -> bool:
    """
    Activate the three jobs:
    1) Message every 1 hour
    2) Message every 2 hours
    3) Join groups every 1 day
    """
    global jobs_started
    if jobs_started:
        return False

    scheduler.add_job(
        send_message, "interval", hours=1, args=[config.MESSAGE_HOURLY],
        id="job_hourly",
    )
    scheduler.add_job(
        send_message, "interval", hours=2, args=[config.MESSAGE_EVERY_2H],
        id="job_every_2h",
    )
    scheduler.add_job(
        join_groups, "interval", days=1,
        id="job_daily_join",
    )

    jobs_started = True
    log.info("All three automation jobs activated.")
    return True


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != config.OWNER_CHAT_ID:
        await update.message.reply_text("⛔ You are not authorized to use this bot.")
        return

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🚀 Start Automation", callback_data="start_jobs")]]
    )
    await update.message.reply_text(
        "Welcome to the control bot 👋\n\n"
        "Press the button below to activate:\n"
        "1️⃣ Message every 1 hour\n"
        "2️⃣ Message every 2 hours\n"
        "3️⃣ Join groups every 1 day",
        reply_markup=keyboard,
    )


async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != config.OWNER_CHAT_ID:
        await query.edit_message_text("⛔ You are not authorized.")
        return

    if query.data == "start_jobs":
        started = start_automation_jobs()
        if started:
            await query.edit_message_text(
                "✅ All jobs activated:\n"
                "1️⃣ Hourly message: ON\n"
                "2️⃣ 2-hour message: ON\n"
                "3️⃣ Daily group join: ON"
            )
        else:
            await query.edit_message_text("⚠️ Jobs are already running.")


async def main():
    await client.start(phone=config.PHONE)
    me = await client.get_me()
    log.info(f"Userbot logged in as: {me.first_name} (@{me.username})")

    scheduler.start()

    app = Application.builder().token(config.CONTROL_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CallbackQueryHandler(on_button))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    log.info("Control bot is running. Send /start in Telegram...")

    try:
        await client.run_until_disconnected()
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
