import pandas as pd

INPUT_FILE = "data/samples/stg_patient_events.csv"
OUTPUT_FILE = "data/samples/rework_analysis.csv"

# Load event data
df = pd.read_csv(INPUT_FILE)

# Count activity occurrences for each patient
activity_counts = (
    df.groupby(["case_id", "activity_name"])
    .size()
    .reset_index(name="activity_count")
)

# Keep only activities that occurred more than once
rework = activity_counts[
    activity_counts["activity_count"] > 1
].copy()

# Sort by patient and activity
rework = rework.sort_values(
    ["case_id", "activity_name"]
)

print("Patients with repeated activities:", rework["case_id"].nunique())

print("\nRework details:")
print(rework.to_string(index=False))

# Save results
rework.to_csv(OUTPUT_FILE, index=False)

print(f"\nSaved to {OUTPUT_FILE}")