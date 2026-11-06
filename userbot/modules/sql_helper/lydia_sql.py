from userbot.modules.sql_helper import DB, to_doc, to_docs, upsert

LYDIA = DB["lydia_ai"]
LYDIA.create_index([("user_id", 1), ("chat_id", 1)], unique=True)


def get_s(user_id, chat_id):
    try:
        return to_doc(LYDIA.find_one({"user_id": user_id, "chat_id": chat_id}))
    except Exception:
        return None


def get_all_s():
    try:
        return to_docs(LYDIA.find())
    except Exception:
        return None


def add_s(user_id, chat_id, session_id, session_expires):
    upsert(
        LYDIA,
        {"user_id": user_id, "chat_id": chat_id},
        {"session_id": session_id, "session_expires": session_expires},
    )


def remove_s(user_id, chat_id):
    LYDIA.delete_one({"user_id": user_id, "chat_id": chat_id})
