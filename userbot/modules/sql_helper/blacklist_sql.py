try:
    from userbot.modules.sql_helper import DB, upsert
except ImportError:
    raise AttributeError
import threading

BLACKLIST = DB["blacklist"]
BLACKLIST.create_index([("chat_id", 1), ("trigger", 1)], unique=True)

BLACKLIST_FILTER_INSERTION_LOCK = threading.RLock()

CHAT_BLACKLISTS = {}


def add_to_blacklist(chat_id, trigger):
    with BLACKLIST_FILTER_INSERTION_LOCK:
        upsert(BLACKLIST, {"chat_id": str(chat_id), "trigger": trigger})
        CHAT_BLACKLISTS.setdefault(str(chat_id), set()).add(trigger)


def rm_from_blacklist(chat_id, trigger):
    with BLACKLIST_FILTER_INSERTION_LOCK:
        result = BLACKLIST.delete_one({"chat_id": str(chat_id), "trigger": trigger})
        if result.deleted_count:
            CHAT_BLACKLISTS.get(str(chat_id), set()).discard(trigger)
            return True

        return False


def get_chat_blacklist(chat_id):
    return CHAT_BLACKLISTS.get(str(chat_id), set())


def num_blacklist_filters():
    return BLACKLIST.count_documents({})


def num_blacklist_chat_filters(chat_id):
    return BLACKLIST.count_documents({"chat_id": str(chat_id)})


def num_blacklist_filter_chats():
    return len(BLACKLIST.distinct("chat_id"))


def __load_chat_blacklists():
    global CHAT_BLACKLISTS
    chats = {}
    for item in BLACKLIST.find():
        chats.setdefault(item["chat_id"], set()).add(item["trigger"])
    CHAT_BLACKLISTS = chats


__load_chat_blacklists()
