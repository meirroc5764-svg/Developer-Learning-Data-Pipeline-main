from confluent_kafka import Producer
from pathlib import Path
import pandas as pd

producer = Producer({
    "bootstrap.servers":"localhost:9092"
})

path = list(Path("C:/Users/Aenigma/OneDrive/Desktop/Developer-Learning-Data-Pipeline-main").rglob("developer_ai_learning_raw.csv"))
print(path[0])

df = pd.read_csv(path[0])


df = df.drop_duplicates()

for _, item in df.iterrows():

    message = item.to_json()
    # print(message)

    producer.produce(
        "notvalidData",
        value=message
    )
producer.flush()