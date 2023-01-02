from google.cloud import tasks_v2
from google.protobuf import duration_pb2

from spinner_scheduler.config import (
    GCP_PROJECT_ID,
    GCP_SCRAPING_CLOUD_TASKS_LOCATION,
    GCP_SCRAPING_CLOUD_TASKS_QUEUE_NAME,
    GCP_SPINDLE_CLOUD_RUN_URL,
    GCP_SPINDLE_INVOKE_SERVICE_ACCOUNT,
)

from .domains import ScraperRunTask

DEADLINE = 900


def create_gcp_task(
    client: tasks_v2.CloudTasksClient, task: ScraperRunTask
) -> tasks_v2.Task:
    http_request = {
        "url": GCP_SPINDLE_CLOUD_RUN_URL,
        "http_method": tasks_v2.HttpMethod.POST,
        "headers": {"Content-type": "application/json"},
        "body": task.json(
            include={"scraper_name", "scraper_inputs", "scraper_run_id"}
        ).encode(),
        "oidc_token": {
            "service_account_email": GCP_SPINDLE_INVOKE_SERVICE_ACCOUNT,
            "audience": GCP_SPINDLE_CLOUD_RUN_URL,
        },
    }
    duration = duration_pb2.Duration()
    duration.FromSeconds(DEADLINE)
    task_to_create = {
        "http_request": http_request,
        "schedule_schedule_time": task.scheduled_datetime.timestamp(),
        "dispatch_deadline": duration,
    }
    response = client.create_task(
        request={"parent": get_gcp_queue_name(client), "task": task_to_create}
    )
    return response


def get_gcp_client() -> tasks_v2.CloudTasksClient:
    return tasks_v2.CloudTasksClient()


def get_gcp_queue_name(client: tasks_v2.CloudTasksClient) -> str:
    return client.queue_path(
        GCP_PROJECT_ID,
        GCP_SCRAPING_CLOUD_TASKS_LOCATION,
        GCP_SCRAPING_CLOUD_TASKS_QUEUE_NAME,
    )
