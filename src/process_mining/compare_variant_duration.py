import pandas as pd

EVENTS_FILE = "data/samples/stg_patient_events.csv"
DURATION_FILE = "data/samples/case_duration.csv"
OUTPUT_FILE = "data/samples/variant_duration.csv"

# Load event data and duration data
events = pd.read_csv(EVENTS_FILE)
duration = pd.read_csv(DURATION_FILE)

# Convert timestamp
events["event_timestamp"] = pd.to_datetime(
    events["event_timestamp"],
    utc=True
)

# Sort events
events = events.sort_values(
    ["case_id", "event_timestamp"]
)

# Create pathway variant for each patient
variants = (
    events.groupby("case_id")["activity_name"]
    .apply(lambda x: " -> ".join(x))
    .reset_index(name="variant")
)

# Combine variants with case duration
case_analysis = variants.merge(
    duration[["case_id", "duration_minutes"]],
    on="case_id",
    how="inner"
)

# Calculate duration statistics for each variant
variant_duration = (
    case_analysis.groupby("variant")["duration_minutes"]
    .agg(
        case_count="count",
        average_duration="mean",
        minimum_duration="min",
        maximum_duration="max"
    )
    .reset_index()
)

# Round duration values
duration_columns = [
    "average_duration",
    "minimum_duration",
    "maximum_duration"
]

variant_duration[duration_columns] = (
    variant_duration[duration_columns]
    .round(2)
)

# Sort by average duration
variant_duration = variant_duration.sort_values(
    "average_duration",
    ascending=False
)

print("Variant duration comparison:")
print(
    variant_duration.to_string(index=False)
)

# Save results
variant_duration.to_csv(
    OUTPUT_FILE,
    index=False
)

print(f"\nSaved to {OUTPUT_FILE}")