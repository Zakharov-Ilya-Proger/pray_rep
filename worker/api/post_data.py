from requests import post


def post_data(record_id, data):
    response = post(
        url='https://molitvamira.ru/api/',
        data={
            "type": "transcribation",
            "pass": "f92R*#eiDF82W@#k2WO",
            "method": "reportSaveTextTranslation",
            "data": {
                "roomID": int(record_id),
                "text": data
            }
        }
    )
    return response
