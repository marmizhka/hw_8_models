import time
import random
from fastapi import FastAPI
from prometheus_client import Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import uvicorn

app = FastAPI()

#создаем метрику "гистограмма задержки"
LATENCY = Histogram("request_latency_seconds", "Request latency in seconds")

@app.get("/predict")
def predict():
    start = time.time()
    #имитируем работу модели: обычно быстро, иногда медленно
    sleep_time = random.uniform(0.1, 0.5)
    if random.random() > 0.8: #в 20% случаев делаем медленно, чтобы сработал алерт
        sleep_time = 1.5 
    time.sleep(sleep_time)
    
    #записываем время выполнения в метрику
    LATENCY.observe(time.time() - start)
    return {"status": "ok", "latency": sleep_time}

@app.get("/metrics")
def metrics():
    #этот эндпоинт читает Prometheus
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
