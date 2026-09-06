import pandas as pd

INPUT_FILE = "data/samples/stg_patient_events.csv"
OUTPUT_FILE = "data/samples/activity_frequency.csv"

# Load event data
df = pd.read_csv(INPUT_FILE)

# Count how many times each activity occurs
activity_counts = (
    df["activity_name"]
    .value_counts()
    .reset_index()
)

activity_counts.columns = ["activity_name", "event_count"]

# Calculate percentage of all events
total_events = activity_counts["event_count"].sum()

activity_counts["percentage"] = (
    activity_counts["event_count"] / total_events * 100
).round(2)

print("Total events:", total_events)

print("\nActivity frequency:")
print(activity_counts.to_string(index=False))

# Save results
activity_counts.to_csv(OUTPUT_FILE, index=False)

print(f"\nSaved to {OUTPUT_FILE}")