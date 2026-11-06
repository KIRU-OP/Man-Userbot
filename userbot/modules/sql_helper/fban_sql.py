try:
    from userbot.modules.sql_helper import DB, to_docs
except ImportError:
    raise AttributeError

FBAN = DB["fban"]
FBAN.create_index("chat_id", unique=True)


def get_flist():
    return to_docs(FBAN.find())


def add_flist(chat_id, fed_name):
    # A plain insert on purpose: adding the same chat twice raises
    # pymongo.errors.DuplicateKeyError, which fban.py handles.
    FBAN.insert_one({"chat_id": str(chat_id), "fed_name": fed_name})


def del_flist(chat_id):
    FBAN.delete_one({"chat_id": str(chat_id)})


def del_flist_all():
    FBAN.delete_many({})
