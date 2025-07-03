from monitoring_toolkit.detectors import get_detector
from monitoring_toolkit.utils.query import Query
from metrics import SUSPICIOUS_COUNT, INFERENCE_TIME

detector = get_detector("confidence", config={"threshold": 0.9})

def monitor_query(payload: dict):
    # Extract data from request
    input_data = payload["input_data"]
    model_output = payload.get("model_output")

    query = Query(input_data=input_data, model_output=model_output)

    with INFERENCE_TIME.time():
        result = detector.process(query)

    if result.is_suspicious:
        SUSPICIOUS_COUNT.inc()

    return {
        "is_suspicious": result.is_suspicious,
        "confidence": result.confidence,
        "reason": result.reason,
        "metadata": result.metadata
    }
