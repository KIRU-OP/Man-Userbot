try:
    from userbot.modules.sql_helper import DB, to_doc
except ImportError:
    raise AttributeError

PMPERMIT = DB["pmpermit"]
PMPERMIT.create_index("chat_id", unique=True)


def is_approved(chat_id):
    try:
        return to_doc(PMPERMIT.find_one({"chat_id": str(chat_id)}))
    except Exception:
        return None


def approve(chat_id):
    # A plain insert on purpose: approving the same chat twice raises
    # pymongo.errors.DuplicateKeyError, which pmpermit.py handles.
    PMPERMIT.insert_one({"chat_id": str(chat_id)})


def dissprove(chat_id):
    PMPERMIT.delete_one({"chat_id": str(chat_id)})
