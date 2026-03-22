import json

from requests import post


def post_data(record_id, data):
    payload = json.dumps({
        "type": "transcribation",
        "pass": "s1Wu4Ot(#@rF8@w2R",
        "method": "reportSaveMediaTranscribation",
        "data": {
            "roomID": int(record_id),
            "transcribation": str(data)
        }
    })
    resp = post(
        url='https://molitvamira.ru/api/',
        data=payload,
        headers={'Content-Type': 'application/json'}
    )
    print(resp.status_code)
    print(resp.text)
    return resp



if __name__ == '__main__':
    response = post_data(1238437720, "Ghfjdgeorij foiawfhaoisf foaisfhiok")

