from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response

REQUEST_COUNT = Counter("api_requests_total", "Total requests to /analyze")
SUSPICIOUS_COUNT = Counter("suspicious_predictions_total", "Number of suspicious detections")
INFERENCE_TIME = Histogram("inference_duration_seconds", "Time taken to process a query")

def setup_metrics(app):
    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        if request.url.path != "/metrics":
            REQUEST_COUNT.inc()
        response = await call_next(request)
        return response

async def metrics_endpoint(request: Request):
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
