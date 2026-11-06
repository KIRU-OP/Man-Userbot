try:
    from userbot.modules.sql_helper import DB, upsert
except ImportError:
    raise Exception("Hello!")

MUTE = DB["mute"]
MUTE.create_index([("sender", 1), ("chat_id", 1)], unique=True)


def is_muted(sender, chat_id):
    user = MUTE.find_one({"sender": str(sender), "chat_id": str(chat_id)})
    return bool(user)


def mute(sender, chat_id):
    upsert(MUTE, {"sender": str(sender), "chat_id": str(chat_id)})


def unmute(sender, chat_id):
    MUTE.delete_one({"sender": str(sender), "chat_id": str(chat_id)})
