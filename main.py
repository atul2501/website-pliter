from telethon import TelegramClient, events
import os
from dotenv import load_dotenv
import re
import asyncio

# Load environment variables from .env
load_dotenv()

# Fetch credentials from .env file
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", 0))  # Channel ID as integer
BOT_CHAT_ID = int(os.getenv("BOT_CHAT_ID", 0))  # Bot's Chat ID
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Your bot token

# Validate credentials
if not all([API_ID, API_HASH, PHONE_NUMBER, CHANNEL_ID, BOT_CHAT_ID, BOT_TOKEN]):
    print("Missing required environment variables")
    exit(1)

# Initialize the userbot client
client = TelegramClient('userbot', API_ID, API_HASH)

# Regex pattern to match URLs
url_pattern = r'https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

@client.on(events.NewMessage(chats=CHANNEL_ID))
async def forward_message(event):
    try:
        print(f"Received message from chat ID {event.chat_id}: {event.message.text}")

        urls = re.findall(url_pattern, event.message.text)
        if urls:
            print(f"Extracted URLs: {urls}")

            # Fetch the group chat entity before sending a message
            group_chat = await client.get_entity(BOT_CHAT_ID)

            for url in urls:
                await client.send_message(group_chat, url)
                print(f"Message forwarded to group ID {BOT_CHAT_ID}: {url}")

    except Exception as e:
        print(f"Error: {e}")


async def main():
    await client.start(phone=PHONE_NUMBER)
    print("Userbot is running...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
