try:
    from userbot.modules.sql_helper import DB, upsert
except ImportError:
    raise AttributeError
import threading

CAT_BROADCAST = DB["catbroadcast"]
CAT_BROADCAST.create_index([("keywoard", 1), ("group_id", 1)], unique=True)

CATBROADCAST_INSERTION_LOCK = threading.RLock()


class BROADCAST_SQL:
    def __init__(self):
        self.BROADCAST_CHANNELS = {}


BROADCAST_SQL_ = BROADCAST_SQL()


def add_to_broadcastlist(keywoard, group_id):
    with CATBROADCAST_INSERTION_LOCK:
        upsert(CAT_BROADCAST, {"keywoard": keywoard, "group_id": str(group_id)})
        BROADCAST_SQL_.BROADCAST_CHANNELS.setdefault(keywoard, set()).add(str(group_id))


def rm_from_broadcastlist(keywoard, group_id):
    with CATBROADCAST_INSERTION_LOCK:
        result = CAT_BROADCAST.delete_one(
            {"keywoard": keywoard, "group_id": str(group_id)}
        )
        if result.deleted_count:
            BROADCAST_SQL_.BROADCAST_CHANNELS.get(keywoard, set()).discard(
                str(group_id)
            )
            return True

        return False


def is_in_broadcastlist(keywoard, group_id):
    with CATBROADCAST_INSERTION_LOCK:
        broadcast_group = CAT_BROADCAST.find_one(
            {"keywoard": keywoard, "group_id": str(group_id)}
        )
        return bool(broadcast_group)


def del_keyword_broadcastlist(keywoard):
    with CATBROADCAST_INSERTION_LOCK:
        CAT_BROADCAST.delete_many({"keywoard": keywoard})
        BROADCAST_SQL_.BROADCAST_CHANNELS.pop(keywoard, None)


def get_chat_broadcastlist(keywoard):
    return BROADCAST_SQL_.BROADCAST_CHANNELS.get(keywoard, set())


def get_broadcastlist_chats():
    return CAT_BROADCAST.distinct("keywoard")


def num_broadcastlist():
    return CAT_BROADCAST.count_documents({})


def num_broadcastlist_chat(keywoard):
    return CAT_BROADCAST.count_documents({"keywoard": keywoard})


def num_broadcastlist_chats():
    return len(CAT_BROADCAST.distinct("keywoard"))


def __load_chat_broadcastlists():
    channels = {}
    for item in CAT_BROADCAST.find():
        channels.setdefault(item["keywoard"], set()).add(item["group_id"])
    BROADCAST_SQL_.BROADCAST_CHANNELS = channels


__load_chat_broadcastlists()
