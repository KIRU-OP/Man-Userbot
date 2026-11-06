try:
    from userbot.modules.sql_helper import DB
except ImportError:
    raise AttributeError
import threading

DEF_COUNT = 0
DEF_LIMIT = 0
DEF_OBJ = (None, DEF_COUNT, DEF_LIMIT)

FLOOD = DB["antiflood"]
FLOOD.create_index("chat_id", unique=True)

INSERTION_LOCK = threading.RLock()

CHAT_FLOOD = {}


def set_flood(chat_id, amount):
    amount = int(amount)
    with INSERTION_LOCK:
        FLOOD.update_one(
            {"chat_id": str(chat_id)},
            {
                "$set": {"user_id": None, "limit": amount},
                "$setOnInsert": {"count": DEF_COUNT},
            },
            upsert=True,
        )

        CHAT_FLOOD[str(chat_id)] = (None, DEF_COUNT, amount)


def update_flood(chat_id: str, user_id) -> bool:
    if str(chat_id) not in CHAT_FLOOD:
        return

    curr_user_id, count, limit = CHAT_FLOOD.get(str(chat_id), DEF_OBJ)

    if limit == 0:  # no antiflood
        return False

    if user_id != curr_user_id or user_id is None:  # other user
        CHAT_FLOOD[str(chat_id)] = (user_id, DEF_COUNT + 1, limit)
        return False

    count += 1
    if count > limit:  # too many msgs, kick
        CHAT_FLOOD[str(chat_id)] = (None, DEF_COUNT, limit)
        return True

    # default -> update
    CHAT_FLOOD[str(chat_id)] = (user_id, count, limit)
    return False


def get_flood_limit(chat_id):
    return CHAT_FLOOD.get(str(chat_id), DEF_OBJ)[2]


def migrate_chat(old_chat_id, new_chat_id):
    with INSERTION_LOCK:
        flood = FLOOD.find_one({"chat_id": str(old_chat_id)})
        if flood:
            CHAT_FLOOD[str(new_chat_id)] = CHAT_FLOOD.get(str(old_chat_id), DEF_OBJ)
            FLOOD.update_one(
                {"chat_id": str(old_chat_id)},
                {"$set": {"chat_id": str(new_chat_id)}},
            )


def __load_flood_settings():
    global CHAT_FLOOD
    CHAT_FLOOD = {
        chat["chat_id"]: (None, DEF_COUNT, chat.get("limit", DEF_LIMIT))
        for chat in FLOOD.find()
    }
    return CHAT_FLOOD
