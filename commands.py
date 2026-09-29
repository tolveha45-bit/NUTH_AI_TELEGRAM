from config import OWNER_ID

from database import (
    set_setting,
    set_blocked,
    set_muted
)


def is_owner(user_id):

    return user_id == OWNER_ID


async def handle_command(event):

    if not event.is_private:
        return False

    sender = await event.get_sender()

    if not sender:
        return False

    if not is_owner(sender.id):
        return False

    text = event.raw_text.strip().lower()

    if text == "/ai_on":

        set_setting(
            "auto_reply",
            "true"
        )

        await event.reply(
            "🤖 AI Auto Reply: ON"
        )

        return True

    if text == "/ai_off":

        set_setting(
            "auto_reply",
            "false"
        )

        await event.reply(
            "⏸️ AI Auto Reply: OFF"
        )

        return True

    if text == "/status":

        status = set_setting

        from database import get_setting

        current = get_setting(
            "auto_reply",
            "true"
        )

        await event.reply(
            f"🤖 Auto Reply: {current.upper()}"
        )

        return True

    if text.startswith("/block "):

        try:
            user_id = int(
                text.split()[1]
            )

            set_blocked(
                user_id,
                True
            )

            await event.reply(
                f"🚫 Blocked: {user_id}"
            )

        except Exception:
            await event.reply(
                "Usage: /block USER_ID"
            )

        return True

    if text.startswith("/unblock "):

        try:
            user_id = int(
                text.split()[1]
            )

            set_blocked(
                user_id,
                False
            )

            await event.reply(
                f"✅ Unblocked: {user_id}"
            )

        except Exception:
            await event.reply(
                "Usage: /unblock USER_ID"
            )

        return True

    if text.startswith("/mute "):

        try:
            user_id = int(
                text.split()[1]
            )

            set_muted(
                user_id,
                True
            )

            await event.reply(
                f"🔇 Muted: {user_id}"
            )

        except Exception:
            await event.reply(
                "Usage: /mute USER_ID"
            )

        return True

    if text.startswith("/unmute "):

        try:
            user_id = int(
                text.split()[1]
            )

            set_muted(
                user_id,
                False
            )

            await event.reply(
                f"🔊 Unmuted: {user_id}"
            )

        except Exception:
            await event.reply(
                "Usage: /unmute USER_ID"
            )

        return True

    return False
