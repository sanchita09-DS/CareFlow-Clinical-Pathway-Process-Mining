# patient_generator.py
# Generates patient journeys using the activity paths defined in activities.py

import csv
import random
from datetime import datetime, timedelta
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
    """
    Generates a list of (Case_ID, Activity_Name, Timestamp) events for multiple patients.
    """
    all_events = []
    base_date = datetime(2026, 8, 1)  # any reference date works

    for i in range(1, num_patients + 1):
        case_id = generate_case_id(i)
        journey = generate_patient_journey()

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

def export_to_csv(events, filename="patient_events.csv"):
    """
    Saves the generated events to a CSV file that can be uploaded to BigQuery.
    """
    with open(filename, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Case_ID", "Activity_Name", "Timestamp"])
        writer.writeheader()
        writer.writerows(events)
    print(f"Exported {len(events)} events to {filename}")

def check_path_distribution(num_patients=300):
    normal_count = 0
    inefficient_count = 0
    for _ in range(num_patients):
        journey = generate_patient_journey()
        if journey == NORMAL_PATH:
            normal_count += 1
        else:
            inefficient_count += 1
    print(f"Normal paths: {normal_count} ({normal_count/num_patients*100:.1f}%)")
    print(f"Inefficient paths: {inefficient_count} ({inefficient_count/num_patients*100:.1f}%)")


def validate_events(events):
    errors = []

    for i, e in enumerate(events):
        if not e.get("Case_ID"):
            errors.append(f"Row {i}: Missing Case_ID")
        if not e.get("Activity_Name"):
            errors.append(f"Row {i}: Missing Activity_Name")
        if not e.get("Timestamp"):
            errors.append(f"Row {i}: Missing Timestamp")

    events_by_case = {}
    for e in events:
        events_by_case.setdefault(e["Case_ID"], []).append(e["Timestamp"])

    for case_id, timestamps in events_by_case.items():
        if timestamps != sorted(timestamps):
            errors.append(f"{case_id}: Timestamps not in chronological order")

    return errors


# Quick test — only runs if you execute this file directly
if __name__ == "__main__":
    events = generate_patients(300)
    print(f"Total events generated: {len(events)}")

    print("\nSample of first 10 events:")
    for event in events[:10]:
        print(event)

    print("\nPath distribution check:")
    check_path_distribution()

    print("\nValidation check:")
    errors = validate_events(events)
    if errors:
        print(f"[FAIL] Found {len(errors)} issues:")
        for err in errors[:10]:
            print(err)
    else:
        print("[PASS] All events passed validation!")

    export_to_csv(events, "../../data/samples/patient_events.csv")