import os
from celery.signals import before_task_publish, task_prerun, task_postrun, setup_logging
from kombu import Exchange, Queue
import structlog
from libs.telemetry import correlation_id_ctx, get_correlation_id, configure_logging

# --- Broker & Backend ---
broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")
result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

# --- Serialization ---
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "Asia/Shanghai"
enable_utc = True
task_track_started = True

# --- Reliability (DLX/DLQ) ---
task_acks_late = True  # Ack only after successful execution (or routing to DLQ)
task_reject_on_worker_lost = True

# Define Exchanges
default_exchange = Exchange("scraper.exchange", type="direct")
dlx_exchange = Exchange("scraper.dlx", type="fanout")

# Define Queues
task_queues = (
    # Main Queue with DLX configuration
    Queue(
        "scraper.tasks",
        default_exchange,
        routing_key="scraper.tasks",
        queue_arguments={
            "x-dead-letter-exchange": "scraper.dlx",
            "x-dead-letter-routing-key": "scraper.dlq",
        },
    ),
    # Dead Letter Queue
    Queue(
        "scraper.dlq",
        dlx_exchange,
        routing_key="scraper.dlq",
    ),
)

task_default_queue = "scraper.tasks"
task_default_exchange = "scraper.exchange"
task_default_routing_key = "scraper.tasks"

# --- Signal Handlers for Tracing ---

@setup_logging.connect
def config_loggers(*args, **kwargs):
    """
    Override Celery's default logging to use structlog.
    """
    configure_logging(json_format=True)

@before_task_publish.connect
def transfer_correlation_id(headers=None, **kwargs):
    """
    Client-side: Inject current correlation_id into task headers before publishing.
    """
    if headers is None:
        headers = {}
    
    cid = get_correlation_id()
    headers["correlation_id"] = cid
    
    # structlog.get_logger().debug("Injecting correlation_id into task", correlation_id=cid)

@task_prerun.connect
def load_correlation_id(task_id, task, *args, **kwargs):
    """
    Worker-side: Extract correlation_id from task headers and set context.
    """
    # Celery request context implies headers are available in task.request
    headers = getattr(task.request, "headers", {}) or {}
    cid = headers.get("correlation_id")
    
    if not cid:
        # If missing (e.g. manual CLI invocation), generate new
        cid = task_id  # fallback to task_id
        
    token = correlation_id_ctx.set(cid)
    task._correlation_token = token
    
    structlog.get_logger().info("Task started", task_name=task.name, task_id=task_id)

@task_postrun.connect
def cleanup_correlation_id(task, **kwargs):
    """
    Worker-side: Clean up context after task execution.
    """
    token = getattr(task, "_correlation_token", None)
    if token:
        correlation_id_ctx.reset(token)
