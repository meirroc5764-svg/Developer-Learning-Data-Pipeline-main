from confluent_kafka import Producer
from pathlib import Path
import json
import csv

producer = Producer({
    "bootstrap.servers":"localhost:9092"
})

path = list(Path("C:/Users/Aenigma/OneDrive/Desktop/Developer-Learning-Data-Pipeline-main").rglob("developer_ai_learning_raw.csv"))
print(path[0])

if not path:
    raise FileNotFoundError("Not Found")

with open(path[0],"r", encoding="utf-8") as f:
    all_data = csv.DictReader(f)

    for data in all_data:

        message = json.dumps(data, ensure_ascii=False)

        producer.produce(
            "notvalidData",
            value=message
        )
        
producer.flush()
print("finish send to kafka")