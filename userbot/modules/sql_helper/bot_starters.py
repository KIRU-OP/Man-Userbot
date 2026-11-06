from userbot.modules.sql_helper import DB, to_doc, to_docs, upsert

BOT_STARTERS = DB["bot_starters"]
BOT_STARTERS.create_index("user_id", unique=True)


def add_starter_to_db(
    user_id,
    first_name,
    date,
    username,
):
    upsert(
        BOT_STARTERS,
        {"user_id": str(user_id)},
        {"first_name": first_name, "date": date, "username": username},
    )
    return True


def del_starter_from_db(user_id):
    result = BOT_STARTERS.delete_one({"user_id": str(user_id)})
    return bool(result.deleted_count)


def get_starter_details(user_id):
    return to_doc(BOT_STARTERS.find_one({"user_id": str(user_id)}))


def get_all_starters():
    try:
        return to_docs(BOT_STARTERS.find())
    except Exception:
        return None
