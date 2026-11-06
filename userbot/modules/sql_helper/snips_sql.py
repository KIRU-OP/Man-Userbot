from userbot.modules.sql_helper import DB, to_doc, to_docs, upsert

SNIPS = DB["snip"]
SNIPS.create_index("keyword", unique=True)


def get_note(keyword):
    return to_doc(SNIPS.find_one({"keyword": keyword}))


def get_notes():
    return to_docs(SNIPS.find())


def add_note(keyword, reply, f_mesg_id):
    """Returns True if the snip is new, False if it replaced an old one."""
    return upsert(SNIPS, {"keyword": keyword}, {"reply": reply, "f_mesg_id": f_mesg_id})


def rm_note(keyword):
    result = SNIPS.delete_one({"keyword": keyword})
    return bool(result.deleted_count)
