from apps.worker_publisher.celery_app import app

@app.task
def publish_content_task(platform_name: str, tenant_id: str, payload: dict):
    print(f"INFO: Publishing to {platform_name} for tenant {tenant_id}")
    # Stub implementation
    return {"status": "published", "platform": platform_name}
