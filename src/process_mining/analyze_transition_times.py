import pandas as pd

INPUT_FILE = "data/samples/stg_patient_events.csv"
OUTPUT_FILE = "data/samples/transition_times.csv"

# Load event data
df = pd.read_csv(INPUT_FILE)

# Convert timestamp
df["event_timestamp"] = pd.to_datetime(
    df["event_timestamp"],
    utc=True
)

# Sort events within each patient
df = df.sort_values(
    ["case_id", "event_timestamp"]
)

# Get the next activity and timestamp for each patient
df["next_activity"] = (
    df.groupby("case_id")["activity_name"]
    .shift(-1)
)

df["next_timestamp"] = (
    df.groupby("case_id")["event_timestamp"]
    .shift(-1)
)

# Calculate time between current and next activity
df["transition_minutes"] = (
    df["next_timestamp"] - df["event_timestamp"]
).dt.total_seconds() / 60

# Remove final activity of each case
transitions = df.dropna(
    subset=["next_activity", "transition_minutes"]
).copy()

# Create transition name
transitions["transition"] = (
    transitions["activity_name"]
    + " -> "
    + transitions["next_activity"]
)

# Calculate transition statistics
transition_summary = (
    transitions.groupby("transition")["transition_minutes"]
    .agg(
        transition_count="count",
        average_minutes="mean",
        minimum_minutes="min",
        maximum_minutes="max"
    )
    .reset_index()
)

# Round values
duration_columns = [
    "average_minutes",
    "minimum_minutes",
    "maximum_minutes"
]

transition_summary[duration_columns] = (
    transition_summary[duration_columns]
    .round(2)
)

# Sort by average transition time
transition_summary = transition_summary.sort_values(
    "average_minutes",
    ascending=False
)

print("Transition time analysis:")
print(
    transition_summary.to_string(index=False)
)

# Save results
transition_summary.to_csv(
    OUTPUT_FILE,
    index=False
)

print(f"\nSaved to {OUTPUT_FILE}")