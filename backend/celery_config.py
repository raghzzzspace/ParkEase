from celery import Celery
# from celery_beat_schedule import beat_schedule  

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker="redis://localhost:6379/0",
        backend="redis://localhost:6379/0",
        include=["tasks.reminder","tasks.monthly_report","tasks.export_csv"]
    )
    
    # celery.conf.update(
    #     app.config,
    #     timezone='Asia/Kolkata',
    #     enable_utc=False,
    #     beat_schedule=beat_schedule,
    #     broker_connection_retry_on_startup=True
    # )

    return celery
