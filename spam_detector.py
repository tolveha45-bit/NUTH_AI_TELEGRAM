import time

user_messages = {}


def is_spam(user_id, message):

    now = time.time()

    if user_id not in user_messages:
        user_messages[user_id] = []

    user_messages[user_id].append(
        (now, message)
    )

    user_messages[user_id] = [
        x for x in user_messages[user_id]
        if now - x[0] < 60
    ]

    recent = user_messages[user_id]

    if len(recent) >= 8:
        return True

    if len(recent) >= 3:

        last_three = [
            x[1].strip().lower()
            for x in recent[-3:]
        ]

        if len(set(last_three)) == 1:
            return True

    return False
