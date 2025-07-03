# MONITAUR 

This is the main repository of the [Monitaur](https://www.netidee.at/monitaur) project, an open-source platform for monitoring AI services. Funded by [Netidee](https://www.netidee.at/).

##  Monitoring API with Prometheus


This is a lightweight, extensible monitoring server built with **FastAPI**, integrated with **Prometheus** for metrics collection. It leverages the reusable [`monitoring_toolkit`](https://github.com/darusik/monitoring_toolkit) package to detect suspicious model inputs (e.g. low-confidence, repetitive, or anomalous queries).


### Features

* Plug-and-play detector system (`monitoring_toolkit`)
* Built-in Prometheus metrics (suspicious counts, confidence scores, errors, etc.)
* FastAPI server to expose detection as an HTTP API
* Docker support for full stack orchestration


### Installation

Clone the repo and start the full monitoring stack:

```bash
git clone https://github.com/your-username/monitoring-api.git
cd monitoring-api
docker compose up --build
```

The API will be running at `http://localhost:8000`, and Prometheus metrics at `http://localhost:9090`.


### API Usage

Send detection requests to the `/detect` endpoint:

```http
POST /detect
Content-Type: application/json

{
  "input_data": "This is a suspicious input",
  "model_output": [0.25, 0.25, 0.25, 0.25],
  "modality": "text"
}
```

You’ll get a response like:

```json
{
  "is_suspicious": true,
  "confidence": 1.38,
  "reason": "entropy mode: suspicious score = 1.3863, threshold = 0.8000"
}
```

#### Quick Testing with `client.py`
You can also test the detection endpoint using the built-in client.py script:

```bash
python app/client.py
```

It will send a few example requests and print the detection results to the console. 

### Prometheus Metrics

Metrics are exposed at `/metrics`. You’ll find:

* `detector_requests_total`: All incoming detection queries
* `suspicious_queries_total`: Total flagged queries
* `detection_confidence_score`: Histogram of confidence scores
* `detector_errors_total`: Internal processing errors

These metrics can be scraped by Prometheus and visualized (e.g. via Grafana).

Metrics can be extended with additional fields from each `DetectionResult`, and customized further depending on the active detector’s behavior (e.g., tracking hash collisions for repetition, or distances for similarity).


### Customization

To switch or extend detectors:

* Modify parameters of `get_detector` in `app/detectors.py`
* Update `metrics.py` accordingly to `DetectionResult` of the new detector 
* All detectors from `monitoring_toolkit` are supported:
  * `confidence`, `repetition`, `similarity`
  * Modal-specific versions: `text_similarity`, `image_repetition`, etc.

Want to add your own? See the toolkit's [README](https://github.com/darusik/monitoring_toolkit) for instructions on writing and registering new detectors.


### Docker Compose Setup

Here's what's inside `docker-compose.yml`:
* `api`: Runs the FastAPI server
* `prometheus`: Collects metrics
<!-- * (Optional later) `grafana`: For rich dashboards -->


### Requirements

* Python 3.10+
* Docker and Docker Compose
* Install Python dependencies via:
    ```bash
    pip install -r requirements.txt
    ```

