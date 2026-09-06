import pandas as pd

INPUT_FILE = "data/samples/stg_patient_events.csv"
OUTPUT_FILE = "data/samples/case_duration.csv"

# Load event data
df = pd.read_csv(INPUT_FILE)

# Convert timestamp
df["event_timestamp"] = pd.to_datetime(
    df["event_timestamp"],
    utc=True
)

# Calculate start and end time for each patient
case_duration = (
    df.groupby("case_id")["event_timestamp"]
    .agg(
        start_time="min",
        end_time="max"
    )
    .reset_index()
)

# Calculate duration in minutes
case_duration["duration_minutes"] = (
    case_duration["end_time"] -
    case_duration["start_time"]
).dt.total_seconds() / 60

# Round duration
case_duration["duration_minutes"] = (
    case_duration["duration_minutes"]
    .round(2)
)

# Sort by duration
case_duration = case_duration.sort_values(
    "duration_minutes"
)

print("Total cases:", len(case_duration))

print("\nCase duration summary:")
print(
    case_duration["duration_minutes"]
    .describe()
    .round(2)
)

print("\nShortest 5 cases:")
print(
    case_duration.head(5).to_string(index=False)
)

print("\nLongest 5 cases:")
print(
    case_duration.tail(5)
    .sort_values("duration_minutes", ascending=False)
    .to_string(index=False)
)

# Save results
case_duration.to_csv(OUTPUT_FILE, index=False)

print(f"\nSaved to {OUTPUT_FILE}")