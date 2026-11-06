try:
    from userbot.modules.sql_helper import DB, to_docs, upsert
except ImportError:
    raise AttributeError

GMUTE = DB["gmute"]
GMUTE.create_index("sender", unique=True)


def is_gmuted(sender_id):
    # Kept as before: returns every gmuted sender, callers filter the list.
    try:
        return to_docs(GMUTE.find())
    except Exception:
        return None


def gmute(sender):
    upsert(GMUTE, {"sender": str(sender)})


def ungmute(sender):
    GMUTE.delete_one({"sender": str(sender)})
