from celery import Celery


app = Celery('tamarcado', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')



@app.task
def soma(a, b):
    import time
    time.sleep(10)
    return a + b