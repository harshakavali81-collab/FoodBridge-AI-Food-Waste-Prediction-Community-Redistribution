"""Basic data-quality reporting before retraining."""
import json
from foodbridge.processing.validation import summarize_quality
def report(csv_path):
    return json.dumps(summarize_quality(csv_path),indent=2)
if __name__=="__main__":print(report("data/synthetic/daily_operations.csv"))
