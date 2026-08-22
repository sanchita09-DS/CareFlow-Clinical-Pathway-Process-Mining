# patient_generator.py
# Generates patient journeys using the activity paths defined in activities.py

import random
from activities import NORMAL_PATH, INEFFICIENT_PATH
from datetime import datetime, timedelta


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

def generate_timestamps(start_time, num_events):
    """
    Generates a list of chronological timestamps for one patient's journey.
    Each event happens 10-40 minutes after the previous one.
    """
    timestamps = [start_time]
    current = start_time
    for _ in range(num_events - 1):
        current = current + timedelta(minutes=random.randint(10, 40))
        timestamps.append(current)
    return timestamps

def generate_patients(num_patients):
    all_events = []
    base_date = datetime(2026, 8, 1)  # any reference date works

    for i in range(1, num_patients + 1):
        case_id = generate_case_id(i)
        journey = generate_patient_journey()

        # random start time for this patient, between 8 AM and 6 PM
        start_time = base_date + timedelta(
            hours=random.randint(8, 18),
            minutes=random.randint(0, 59)
        )

        timestamps = generate_timestamps(start_time, len(journey))

        for activity, ts in zip(journey, timestamps):
            all_events.append({
                "Case_ID": case_id,
                "Activity_Name": activity,
                "Timestamp": ts.strftime("%Y-%m-%d %H:%M:%S")
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


