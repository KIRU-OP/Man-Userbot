from userbot.modules.sql_helper import DB, to_doc, to_docs, upsert

FILTERS = DB["filters"]
FILTERS.create_index([("chat_id", 1), ("keyword", 1)], unique=True)


def get_filter(chat_id, keyword):
    return to_doc(FILTERS.find_one({"chat_id": str(chat_id), "keyword": keyword}))


def get_filters(chat_id):
    return to_docs(FILTERS.find({"chat_id": str(chat_id)}))


def add_filter(chat_id, keyword, reply, f_mesg_id):
    """Returns True if the filter is new, False if it replaced an old one."""
    return upsert(
        FILTERS,
        {"chat_id": str(chat_id), "keyword": keyword},
        {"reply": reply, "f_mesg_id": f_mesg_id},
    )


def remove_filter(chat_id, keyword):
    result = FILTERS.delete_one({"chat_id": str(chat_id), "keyword": keyword})
    return bool(result.deleted_count)


def remove_all_filters(chat_id):
    FILTERS.delete_many({"chat_id": str(chat_id)})
