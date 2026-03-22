from worker.tasks import process

def process_request(data: dict) -> None:
    process(data['req_id'], data['hash'])
