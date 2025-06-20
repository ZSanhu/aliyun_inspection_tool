from datetime import datetime, timedelta
import json

def load_config(path="./config.json"):
    with open(path, 'r') as f:
        return json.load(f)

def get_time_range():
    """
    返回默认时间范围：今天 00:00 到 当前时间（UTC 格式）
    """
    now = datetime.utcnow()
    start = datetime(now.year, now.month, now.day)
    return start.strftime("%Y-%m-%dT%H:%M:%SZ"), now.strftime("%Y-%m-%dT%H:%M:%SZ")
