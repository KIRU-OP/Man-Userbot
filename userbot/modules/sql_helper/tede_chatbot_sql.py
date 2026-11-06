import threading

from userbot.modules.sql_helper import DB, upsert

TEDE_CHATBOT = DB["tede_chatbot"]
TEDE_CHATBOT.create_index("chat_id", unique=True)

INSERTION_LOCK = threading.RLock()


def is_tede(chat_id):
    return bool(TEDE_CHATBOT.find_one({"chat_id": str(chat_id)}))


def set_tede(chat_id):
    with INSERTION_LOCK:
        upsert(TEDE_CHATBOT, {"chat_id": str(chat_id)})


def rem_tede(chat_id):
    with INSERTION_LOCK:
        TEDE_CHATBOT.delete_one({"chat_id": str(chat_id)})
