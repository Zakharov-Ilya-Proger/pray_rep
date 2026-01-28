from worker.tasks import process

def process_request(req_id: str, hash: str):
    process(req_id, hash)
