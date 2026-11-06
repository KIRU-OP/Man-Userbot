from userbot.modules.sql_helper import DB, to_doc, to_docs, upsert

BOT_BLACKLIST = DB["bot_blacklist"]
BOT_BLACKLIST.create_index("chat_id", unique=True)


def add_user_to_bl(
    chat_id: int, first_name: str, username: str, reason: str, date: str
):
    """add the user to the blacklist (or refresh the existing entry)"""
    upsert(
        BOT_BLACKLIST,
        {"chat_id": str(chat_id)},
        {
            "first_name": first_name,
            "username": username,
            "reason": reason,
            "date": date,
        },
    )
    return True


def check_is_black_list(chat_id: int):
    """check if user_id is blacklisted"""
    return to_doc(BOT_BLACKLIST.find_one({"chat_id": str(chat_id)}))


def rem_user_from_bl(chat_id: int):
    """remove the user from the blacklist"""
    result = BOT_BLACKLIST.delete_one({"chat_id": str(chat_id)})
    return bool(result.deleted_count)


def get_all_bl_users():
    try:
        return to_docs(BOT_BLACKLIST.find())
    except Exception:
        return None
