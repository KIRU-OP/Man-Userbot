try:
    from userbot.modules.sql_helper import DB, upsert
except ImportError:
    raise AttributeError
import threading

WARNS = DB["warns"]
WARNS.create_index([("user_id", 1), ("chat_id", 1)], unique=True)

WARN_SETTINGS = DB["warn_settings"]
WARN_SETTINGS.create_index("chat_id", unique=True)

WARN_INSERTION_LOCK = threading.RLock()
WARN_SETTINGS_LOCK = threading.RLock()


def _key(user_id, chat_id):
    return {"user_id": int(user_id), "chat_id": str(chat_id)}


def warn_user(user_id, chat_id, reason=None):
    with WARN_INSERTION_LOCK:
        key = _key(user_id, chat_id)
        warned_user = WARNS.find_one(key) or {"num_warns": 0, "reasons": ""}

        num = warned_user["num_warns"] + 1
        reasons = warned_user["reasons"]
        if reason:
            reasons = reasons + "\r\n\r\n" + reason

        upsert(WARNS, key, {"num_warns": num, "reasons": reasons})

        return num, reasons


def remove_warn(user_id, chat_id):
    with WARN_INSERTION_LOCK:
        key = _key(user_id, chat_id)
        warned_user = WARNS.find_one(key)

        if warned_user and warned_user["num_warns"] > 0:
            WARNS.update_one(key, {"$inc": {"num_warns": -1}})
            return True

        return False


def reset_warns(user_id, chat_id):
    with WARN_INSERTION_LOCK:
        WARNS.update_one(
            _key(user_id, chat_id), {"$set": {"num_warns": 0, "reasons": ""}}
        )


def get_warns(user_id, chat_id):
    user = WARNS.find_one(_key(user_id, chat_id))
    if not user:
        return None
    return user["num_warns"], user["reasons"]


def set_warn_limit(chat_id, warn_limit):
    with WARN_SETTINGS_LOCK:
        WARN_SETTINGS.update_one(
            {"chat_id": str(chat_id)},
            {
                "$set": {"warn_limit": int(warn_limit)},
                "$setOnInsert": {"soft_warn": False},
            },
            upsert=True,
        )


def set_warn_strength(chat_id, soft_warn):
    with WARN_SETTINGS_LOCK:
        WARN_SETTINGS.update_one(
            {"chat_id": str(chat_id)},
            {
                "$set": {"soft_warn": bool(soft_warn)},
                "$setOnInsert": {"warn_limit": 3},
            },
            upsert=True,
        )


def get_warn_setting(chat_id):
    setting = WARN_SETTINGS.find_one({"chat_id": str(chat_id)})
    if setting:
        return setting["warn_limit"], setting["soft_warn"]
    return 3, False


def num_warns():
    result = list(WARNS.aggregate([{"$group": {"_id": None, "n": {"$sum": "$num_warns"}}}]))
    return result[0]["n"] if result else 0


def num_warn_chats():
    return len(WARNS.distinct("chat_id"))
