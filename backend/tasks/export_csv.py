from celery_worker import celery

@celery.task(name='tasks.export_csv.export_parking_history_to_csv')
def export_parking_history_to_csv(email, data):
    import pandas as pd, os
    from datetime import datetime

    df = pd.DataFrame(data)
    filename = f"{email.replace('@', '_')}_{int(datetime.utcnow().timestamp())}.csv"
    
    # absolute path
    export_dir = os.path.join(os.path.dirname(__file__), "..", "exports")
    export_dir = os.path.abspath(export_dir)
    os.makedirs(export_dir, exist_ok=True)

    file_path = os.path.join(export_dir, filename)
    df.to_csv(file_path, index=False)

    return filename

