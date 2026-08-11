# activities.py
# Master list of hospital activities used to generate patient journeys

ACTIVITIES = [
    "Registration",
    "Triage",
    "Doctor",
    "Blood Test",
    "X-Ray",
    "Pharmacy",
    "Discharge"
]

# A "normal" journey — patient goes through in a straight line, no repeats
NORMAL_PATH = [
    "Registration",
    "Triage",
    "Doctor",
    "Discharge"
]

# An "inefficient" journey — includes a loop-back (this is what CareFlow is meant to catch)
INEFFICIENT_PATH = [
    "Registration",
    "Triage",
    "Doctor",
    "X-Ray",
    "Triage",     # ← loop-back: patient sent back to Triage
    "Doctor",
    "Discharge"
]
