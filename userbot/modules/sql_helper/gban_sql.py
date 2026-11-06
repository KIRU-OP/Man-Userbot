from userbot.modules.sql_helper import DB, to_doc, to_docs, upsert

GBAN = DB["gban"]
GBAN.create_index("chat_id", unique=True)


def is_gbanned(chat_id):
    try:
        return to_doc(GBAN.find_one({"chat_id": str(chat_id)}))
    except Exception:
        return None


def get_gbanuser(chat_id):
    return to_doc(GBAN.find_one({"chat_id": str(chat_id)}))


def freakgban(chat_id, reason):
    upsert(GBAN, {"chat_id": str(chat_id)}, {"reason": str(reason)})


def freakungban(chat_id):
    GBAN.delete_one({"chat_id": str(chat_id)})


def get_all_gbanned():
    return to_docs(GBAN.find())
