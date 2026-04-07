from celery import shared_task
import requests
import time
from .rate_limiter import consume_token
from .queue_manager import get_all_customers, pop_request

EXTERNAL_API = "https://example.com/api"

@shared_task(bind=True, max_retries=5)
def process_requests(self):
    customers = get_all_customers()

    for customer in customers:
        if not consume_token():
            time.sleep(1)
            return process_requests.delay()

        request_data = pop_request(customer)
        if not request_data:
            continue

        try:
            response = requests.post(EXTERNAL_API, json=request_data, timeout=5)

            if response.status_code >= 500:
                raise Exception("Server Error")

            print(f"Success for {customer}: {response.json()}")

        except Exception as e:
            try:
                self.retry(countdown=2 ** self.request.retries)
            except self.MaxRetriesExceededError:
                print(f"Failed permanently: {customer}")
