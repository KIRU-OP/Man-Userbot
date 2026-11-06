try:
    from userbot.modules.sql_helper import DB, to_doc, upsert
except ImportError:
    raise AttributeError

WELCOME = DB["welcome"]
WELCOME.create_index("chat_id", unique=True)


def get_welcome(chat_id):
    return to_doc(WELCOME.find_one({"chat_id": str(chat_id)}))


def get_current_welcome_settings(chat_id):
    try:
        return to_doc(WELCOME.find_one({"chat_id": str(chat_id)}))
    except Exception:
        return None


def add_welcome_setting(chat_id, previous_welcome, reply, f_mesg_id):
    """Returns True if the setting is new, False if it replaced an old one."""
    return upsert(
        WELCOME,
        {"chat_id": str(chat_id)},
        {
            "previous_welcome": previous_welcome,
            "reply": reply,
            "f_mesg_id": f_mesg_id,
        },
    )


def rm_welcome_setting(chat_id):
    try:
        result = WELCOME.delete_one({"chat_id": str(chat_id)})
        return bool(result.deleted_count)
    except Exception:
        return False


def update_previous_welcome(chat_id, previous_welcome):
    WELCOME.update_one(
        {"chat_id": str(chat_id)}, {"$set": {"previous_welcome": previous_welcome}}
    )
