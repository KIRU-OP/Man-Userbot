try:
    from userbot.modules.sql_helper import DB, upsert
except ImportError:
    raise AttributeError

GLOBALS = DB["globals"]
GLOBALS.create_index("variable", unique=True)


def gvarstatus(variable):
    try:
        return GLOBALS.find_one({"variable": str(variable)})["value"]
    except Exception:
        return None


def addgvar(variable, value):
    upsert(GLOBALS, {"variable": str(variable)}, {"value": value})


def delgvar(variable):
    GLOBALS.delete_many({"variable": str(variable)})
