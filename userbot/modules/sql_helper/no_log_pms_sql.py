from userbot.modules.sql_helper import DB, to_doc, upsert

NO_LOG_PMS = DB["no_log_pms"]
NO_LOG_PMS.create_index("chat_id", unique=True)


def is_approved(chat_id):
    try:
        return to_doc(NO_LOG_PMS.find_one({"chat_id": chat_id}))
    except Exception:
        return None


def approve(chat_id):
    upsert(NO_LOG_PMS, {"chat_id": chat_id})


def disapprove(chat_id):
    NO_LOG_PMS.delete_one({"chat_id": chat_id})
