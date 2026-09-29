import asyncio
import time

from config import (
    REPLY_DELAY,
    OWNER_PAUSE_SECONDS
)

from ai import generate_reply

from database import (
    add_user,
    is_blocked,
    is_muted
)

from spam_detector import is_spam


last_owner_activity = {}


def owner_is_active(user_id):

    last_time = last_owner_activity.get(
        user_id,
        0
    )

    return (
        time.time() - last_time
        < OWNER_PAUSE_SECONDS
    )


def mark_owner_activity(user_id):

    last_owner_activity[user_id] = time.time()


async def process_message(event):

    if not event.is_private:
        return

    sender = await event.get_sender()

    if not sender:
        return

    user_id = sender.id

    # Ignore own messages
    if sender.is_self:
        mark_owner_activity(user_id)
        return

    add_user(
        user_id,
        getattr(sender, "username", ""),
        getattr(sender, "first_name", "")
    )

    if is_blocked(user_id):
        return

    if is_muted(user_id):
        return

    text = event.raw_text.strip()

    if not text:
        return

    if is_spam(user_id, text):

        await event.reply(
            "⚠️ Please avoid sending repeated messages."
        )

        return

    if owner_is_active(user_id):
        return

    await asyncio.sleep(REPLY_DELAY)

    try:

        reply = generate_reply(
            user_id,
            text
        )

        await event.reply(reply)

    except Exception as error:

        print(
            f"[AI ERROR] {error}"
        )
