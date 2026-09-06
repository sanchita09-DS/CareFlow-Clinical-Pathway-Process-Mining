import pandas as pd

INPUT_FILE = "data/samples/stg_patient_events.csv"
OUTPUT_FILE = "data/samples/process_variants.csv"

# Load event data
df = pd.read_csv(INPUT_FILE)

# Convert timestamp
df["event_timestamp"] = pd.to_datetime(
    df["event_timestamp"],
    utc=True
)

# Sort events within each patient case
df = df.sort_values(
    ["case_id", "event_timestamp"]
)

# Create a pathway for each case
variants = (
    df.groupby("case_id")["activity_name"]
    .apply(lambda x: " -> ".join(x))
    .reset_index(name="variant")
)

# Count how many cases follow each variant
variant_counts = (
    variants.groupby("variant")
    .size()
    .reset_index(name="case_count")
    .sort_values("case_count", ascending=False)
)

# Calculate percentage of cases
total_cases = variant_counts["case_count"].sum()

variant_counts["percentage"] = (
    variant_counts["case_count"] / total_cases * 100
).round(2)

# Add rank
variant_counts.insert(
    0,
    "variant_rank",
    range(1, len(variant_counts) + 1)
)

print("Total cases:", total_cases)
print("Unique variants:", len(variant_counts))

print("\nTop 10 variants:")
print(variant_counts.head(10).to_string(index=False).encode("utf-8", errors="replace").decode("utf-8"))
# Save results
variant_counts.to_csv(OUTPUT_FILE, index=False)

print(f"\nSaved to {OUTPUT_FILE}")