import pandas as pd

VARIANTS_FILE = "data/samples/process_variants.csv"
DURATION_FILE = "data/samples/variant_duration.csv"
REWORK_FILE = "data/samples/rework_analysis.csv"
TRANSITION_FILE = "data/samples/transition_times.csv"

OUTPUT_FILE = "data/samples/process_summary.csv"

# Load analysis results
variants = pd.read_csv(VARIANTS_FILE)
duration = pd.read_csv(DURATION_FILE)
rework = pd.read_csv(REWORK_FILE)
transitions = pd.read_csv(TRANSITION_FILE)

# Basic metrics
total_cases = variants["case_count"].sum()
unique_variants = len(variants)
rework_cases = rework["case_id"].nunique()

# Standard and rework variants
standard = variants[
    variants["variant"].str.contains(
        "X-Ray",
        case=False,
        na=False
    ) == False
]

xray = variants[
    variants["variant"].str.contains(
        "X-Ray",
        case=False,
        na=False
    )
]

standard_cases = standard["case_count"].sum()
xray_cases = xray["case_count"].sum()

# Average durations
standard_duration = duration[
    duration["variant"].str.contains(
        "X-Ray",
        case=False,
        na=False
    ) == False
]["average_duration"].mean()

xray_duration = duration[
    duration["variant"].str.contains(
        "X-Ray",
        case=False,
        na=False
    )
]["average_duration"].mean()

# Longest transition
longest_transition = transitions.iloc[0]

# Create summary table
summary = pd.DataFrame({
    "metric": [
        "Total cases",
        "Unique variants",
        "Rework cases",
        "Standard pathway cases",
        "X-Ray pathway cases",
        "Standard pathway average duration (min)",
        "X-Ray pathway average duration (min)",
        "Longest average transition",
        "Longest average transition time (min)"
    ],
    "value": [
        total_cases,
        unique_variants,
        rework_cases,
        standard_cases,
        xray_cases,
        round(standard_duration, 2),
        round(xray_duration, 2),
        longest_transition["transition"],
        longest_transition["average_minutes"]
    ]
})

print("CareFlow Process Mining Summary")
print("=" * 40)
print(summary.to_string(index=False))

# Save summary
summary.to_csv(OUTPUT_FILE, index=False)

print(f"\nSaved to {OUTPUT_FILE}")