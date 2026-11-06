try:
    from userbot.modules.sql_helper import DB, to_docs, upsert
except ImportError:
    raise AttributeError

MUTED = DB["muted"]
MUTED.create_index([("chat_id", 1), ("sender", 1)], unique=True)


def is_muted(chat_id):
    try:
        return to_docs(MUTED.find({"chat_id": str(chat_id)}))
    except Exception:
        return None


def mute(chat_id, sender):
    upsert(MUTED, {"chat_id": str(chat_id), "sender": str(sender)})


def unmute(chat_id, sender):
    MUTED.delete_one({"chat_id": str(chat_id), "sender": str(sender)})
