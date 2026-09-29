import asyncio

from telethon import TelegramClient, events

from config import (
    TG_API_ID,
    TG_API_HASH,
    TG_PHONE,
    AUTO_REPLY
)

from database import init_db, get_setting

from auto_reply import process_message

from commands import handle_command


SESSION_NAME = "nuth_personal"


client = TelegramClient(
    SESSION_NAME,
    TG_API_ID,
    TG_API_HASH
)


@client.on(
    events.NewMessage(
        incoming=True
    )
)
async def incoming_message(event):

    # Owner commands
    handled = await handle_command(
        event
    )

    if handled:
        return

    if not AUTO_REPLY:
        return

    status = get_setting(
        "auto_reply",
        "true"
    )

    if status != "true":
        return

    await process_message(
        event
    )


async def main():

    init_db()

    print(
        "================================"
    )

    print(
        "      NUTH AI TELEGRAM"
    )

    print(
        "   Personal Auto Reply System"
    )

    print(
        "================================"
    )

    await client.start(
        phone=TG_PHONE
    )

    me = await client.get_me()

    print(
        f"Logged in as: "
        f"{me.first_name} "
        f"(ID: {me.id})"
    )

    print(
        "🤖 Auto Reply is running..."
    )

    await client.run_until_disconnected()


if __name__ == "__main__":

    asyncio.run(main())
