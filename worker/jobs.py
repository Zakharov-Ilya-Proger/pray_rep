from worker.tasks import process

def process_request(data: dict):
    process(data['req_id'], data['hash'])
