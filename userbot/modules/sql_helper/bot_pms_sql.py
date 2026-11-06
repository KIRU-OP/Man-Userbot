from userbot.modules.sql_helper import DB, to_docs, upsert

BOT_PMS = DB["bot_pms_data"]
BOT_PMS.create_index([("message_id", 1), ("result_id", 1)], unique=True)


def _int(value):
    return None if value is None else int(value)


def add_user_to_db(message_id, first_name, chat_id, reply_id, logger_id, result_id):
    upsert(
        BOT_PMS,
        {"message_id": _int(message_id), "result_id": _int(result_id)},
        {
            "first_name": first_name,
            "chat_id": str(chat_id),
            "reply_id": _int(reply_id),
            "logger_id": _int(logger_id),
        },
    )
    return True


def _find(field, value):
    result = to_docs(BOT_PMS.find({field: _int(value)}))
    return result or None


def get_user_id(message_id):
    return _find("message_id", message_id)


def del_user_from_db(message_id):
    result = BOT_PMS.delete_many({"message_id": _int(message_id)})
    return bool(result.deleted_count)


def get_user_reply(reply_id):
    return _find("reply_id", reply_id)


def get_user_results(result_id):
    return _find("result_id", result_id)


def get_user_logging(logger_id):
    return _find("logger_id", logger_id)
