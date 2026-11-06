try:
    from userbot.modules.sql_helper import DB, to_doc, to_docs, upsert
except ImportError:
    raise AttributeError

NOTES = DB["notes"]
NOTES.create_index([("chat_id", 1), ("keyword", 1)], unique=True)


def get_note(chat_id, keyword):
    return to_doc(NOTES.find_one({"chat_id": str(chat_id), "keyword": keyword}))


def get_notes(chat_id):
    return to_docs(NOTES.find({"chat_id": str(chat_id)}))


def add_note(chat_id, keyword, reply, f_mesg_id):
    """Returns True if the note is new, False if it replaced an old one."""
    return upsert(
        NOTES,
        {"chat_id": str(chat_id), "keyword": keyword},
        {"reply": reply, "f_mesg_id": f_mesg_id},
    )


def rm_note(chat_id, keyword):
    result = NOTES.delete_one({"chat_id": str(chat_id), "keyword": keyword})
    return bool(result.deleted_count)
