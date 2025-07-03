import requests
import time
import random

URL = "http://localhost:8000/detect"  # Adjust if running elsewhere

EXAMPLES = [
    {"input_data": "This is a suspicious input", "model_output": [0.25, 0.25, 0.25, 0.25]},  # High entropy
    {"input_data": "This is a confident prediction", "model_output": [0.9, 0.05, 0.05]},     # Low entropy
    {"input_data": "Might be uncertain", "model_output": [0.4, 0.3, 0.3]},
    {"input_data": "Very confident", "model_output": [0.99, 0.005, 0.005]},
]

def send_query(data):
    try:
        response = requests.post(URL, json=data)
        response.raise_for_status()
        result = response.json()
        print(f"Input: {data['input_data'][:30]:<30} | Suspicious: {result['is_suspicious']} | Confidence: {result['confidence']:.4f}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    for i in range(10):
        query = random.choice(EXAMPLES)
        send_query(query)
        time.sleep(1)