# patient_generator.py
# Generates patient journeys using the activity paths defined in activities.py

import random
from activities import NORMAL_PATH, INEFFICIENT_PATH


def generate_case_id(patient_number):
    """
    Turns a number into a Case_ID like P001, P002, ...
    """
    return f"P{patient_number:03d}"


def generate_patient_journey():
    """
    Randomly picks a normal or inefficient path for one patient.
    80% of patients follow the normal path, 20% hit a loop-back.
    """
    if random.random() < 0.8:
        return NORMAL_PATH
    else:
        return INEFFICIENT_PATH


def generate_patients(num_patients):
    """
    Generates a list of (Case_ID, Activity_Name) pairs for multiple patients.
    Timestamps will be added in Day 3 — this is just the structure for now.
    """
    all_events = []

    for i in range(1, num_patients + 1):
        case_id = generate_case_id(i)
        journey = generate_patient_journey()

        for activity in journey:
            all_events.append({
                "Case_ID": case_id,
                "Activity_Name": activity
            })

    return all_events


# Quick test — only runs if you execute this file directly
if __name__ == "__main__":
    events = generate_patients(300)
    # for event in events:
    #     print(event)
    print(f"Total events generated: {len(events)}")
    print("Sample of first 10 events:")
    for event in events[:10]:
        print(event)