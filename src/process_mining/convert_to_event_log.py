import pandas as pd
import pm4py

INPUT_FILE = "data/samples/stg_patient_events.csv"

df = pd.read_csv(INPUT_FILE)

df = df.rename(columns={
    "case_id": "case:concept:name",
    "activity_name": "concept:name",
    "event_timestamp": "time:timestamp",
})

df["time:timestamp"] = pd.to_datetime(df["time:timestamp"], utc=True)

event_log = pm4py.convert_to_event_log(df)

print(f"Number of cases: {len(event_log)}")
print(f"Number of events: {len(df)}")

print("\nFirst case:")
print(event_log[0])