# Note: scheduler also has access to app context with scheduler.app.app_context()
import os
from src.extensions import scheduler

file_queue = []

@scheduler.task(
    "interval",
    id="delete_image_files",
    seconds=int(os.getenv("FILE_DELETE_INTERVAL", default=86400)),
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def delete_image_files():
    print("running delete images")
    while len(file_queue) > 0:
        file = file_queue.pop()
        os.remove(file)

