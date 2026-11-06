from userbot.modules.sql_helper import DB, to_doc, to_docs, upsert

COLLECTIONS = DB["cat_globalcollectionjson"]
COLLECTIONS.create_index("keywoard", unique=True)


def _clean(value):
    """BSON only allows string keys, so stringify dict keys recursively."""
    if isinstance(value, dict):
        return {str(k): _clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_clean(v) for v in value]
    return value


def get_collection(keywoard):
    return to_doc(COLLECTIONS.find_one({"keywoard": keywoard}))


def add_collection(keywoard, json, njson=None):
    upsert(
        COLLECTIONS,
        {"keywoard": keywoard},
        {"json": _clean(json), "njson": _clean(njson or {})},
    )
    return True


def del_collection(keywoard):
    result = COLLECTIONS.delete_one({"keywoard": keywoard})
    return bool(result.deleted_count)


def get_collections():
    return to_docs(COLLECTIONS.find())
