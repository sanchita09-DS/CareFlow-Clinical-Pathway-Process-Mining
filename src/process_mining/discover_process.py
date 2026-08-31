import pandas as pd
import pm4py
from pm4py.algo.discovery.inductive import algorithm as inductive_miner

INPUT_FILE = "data/samples/stg_patient_events.csv"

df = pd.read_csv(INPUT_FILE)

df = df.rename(columns={
    "case_id": "case:concept:name",
    "activity_name": "concept:name",
    "event_timestamp": "time:timestamp",
})

df["time:timestamp"] = pd.to_datetime(
    df["time:timestamp"],
    utc=True
)

event_log = pm4py.convert_to_event_log(df)

print(f"Cases: {len(event_log)}")
print(f"Events: {len(df)}")

process_tree = inductive_miner.apply(event_log)

print("\nProcess model discovered successfully.")
print(process_tree)