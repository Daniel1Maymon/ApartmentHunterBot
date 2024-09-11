import celery

@celery.task
def print_message(message):
    print(f"Task is running: {message}")
    return f"Message '{message}' printed!"
