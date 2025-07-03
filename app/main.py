# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from monitoring_toolkit.detectors import get_detector
from monitoring_toolkit.utils.query import Query

from prometheus_client import Counter, Histogram, make_asgi_app
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.responses import Response
from starlette.requests import Request

import uvicorn

# ---- Prometheus Custom Metrics ----

# Total number of requests
REQUEST_COUNT = Counter(
    "detector_requests_total", 
    "Total number of detection requests",
    ["detector"]
)

# Number of suspicious queries detected
SUSPICIOUS_COUNT = Counter(
    "suspicious_queries_total",
    "Total number of suspicious queries",
    ["detector"]
)

# Distribution of scores
SCORE_HISTOGRAM = Histogram(
    "detection_confidence_score", 
    "Distribution of suspiciousness confidence scores",
    ["detector"]
)

# Error counter for failed requests
ERROR_COUNTER = Counter(
    "detector_errors_total",
    "Total number of errors encountered during detection",
    ["detector"]
)

# ---- FastAPI Setup ----

app = FastAPI(title="Monitoring")

# Replace with your actual detector name and config
DETECTOR_NAME = "confidence"
detector = get_detector(DETECTOR_NAME, config={"mode": "entropy", "threshold": 0.8})

# Enable Prometheus instrumentation
Instrumentator().instrument(app).expose(app)


# ---- API Models ----

class QueryRequest(BaseModel):
    input_data: str
    model_output: list


# ---- Routes ----

@app.post("/detect")
async def detect(request: QueryRequest):
    try:
        query = Query(
            input_data=request.input_data,
            model_output=request.model_output,
        )
        result = detector.process(query)

        # Update Prometheus metrics
        REQUEST_COUNT.labels(DETECTOR_NAME).inc()
        SCORE_HISTOGRAM.labels(DETECTOR_NAME).observe(result.confidence)
        if result.is_suspicious:
            SUSPICIOUS_COUNT.labels(DETECTOR_NAME).inc()

        return result.dict()
    except Exception as e:
        ERROR_COUNTER.labels(DETECTOR_NAME).inc()
        raise HTTPException(status_code=500, detail=str(e))


# Optional: health check
@app.get("/health")
async def health():
    return {"status": "ok"}

app.mount("/metrics", make_asgi_app())


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
