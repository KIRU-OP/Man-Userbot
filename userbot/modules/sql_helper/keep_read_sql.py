try:
    from userbot.modules.sql_helper import DB, to_docs, upsert
except ImportError:
    raise AttributeError

KREAD = DB["kread"]
KREAD.create_index("groupid", unique=True)


def is_kread():
    try:
        return to_docs(KREAD.find())
    except Exception:
        return None


def kread(chat):
    upsert(KREAD, {"groupid": str(chat)})


def unkread(chat):
    KREAD.delete_one({"groupid": str(chat)})
