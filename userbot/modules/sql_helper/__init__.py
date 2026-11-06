"""MongoDB storage layer.

Every ``*_sql`` helper module in this package used to sit on top of SQLAlchemy.
They now use pymongo, but keep the same public functions, arguments and return
shapes, so the rest of the userbot does not need to change.

Importing this package raises ``AttributeError`` when MONGO_URI is not set.
Callers rely on that to run in "non-database mode".
"""

from pymongo import MongoClient
from pymongo.errors import ConfigurationError, DuplicateKeyError

from userbot import MONGO_DB_NAME, MONGO_URI

if not MONGO_URI:
    raise AttributeError("MONGO_URI is not configured")


class Doc(dict):
    """A dict whose keys can also be read as attributes (``row.chat_id``)."""

    __slots__ = ()

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name) from None

    def __setattr__(self, name, value):
        self[name] = value


def to_doc(raw):
    """Turn a raw Mongo document into a Doc (without ``_id``), or None."""
    if not raw:
        return None
    raw = dict(raw)
    raw.pop("_id", None)
    return Doc(raw)


def to_docs(cursor):
    return [to_doc(raw) for raw in cursor]


def upsert(collection, key, fields=None):
    """Insert or replace the document identified by ``key``.

    Returns True when a new document was created, False when one was replaced.
    """
    document = {**key, **(fields or {})}
    try:
        result = collection.replace_one(key, document, upsert=True)
    except DuplicateKeyError:  # two upserts raced each other, so retry once
        result = collection.replace_one(key, document, upsert=True)
    return result.upserted_id is not None


def start():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=15000)
    try:
        client.admin.command("ping")
    except Exception as e:
        print("Tidak bisa terhubung ke MongoDB. Cek MONGO_URI dan Network Access.")
        print(str(e))
        raise
    if MONGO_DB_NAME:
        return client[MONGO_DB_NAME]
    try:
        return client.get_default_database()
    except ConfigurationError:
        return client["man_userbot"]


DB = start()
