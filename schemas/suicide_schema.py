def suicide_queryEntity(item) -> dict:
    return {
     "user_text": str(item["_id"]),
    }


def suicide_queriesEntity(items) -> list:
    return [suicide_queryEntity(item) for item in items]