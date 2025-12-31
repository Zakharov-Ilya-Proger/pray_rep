from worker.tasks import process

def process_request(req_id: str):
    process(req_id)
