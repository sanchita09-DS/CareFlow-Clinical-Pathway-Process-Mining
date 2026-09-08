import pandas as pd
import pm4py

from pm4py.objects.process_tree.obj import ProcessTree, Operator
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay


# --------------------------------------------------
# 1. Load patient event data
# --------------------------------------------------

df = pd.read_csv("data/samples/stg_patient_events.csv")

df = df.rename(columns={
    "case_id": "case:concept:name",
    "activity_name": "concept:name",
    "event_timestamp": "time:timestamp"
})

df["time:timestamp"] = pd.to_datetime(df["time:timestamp"])

# Sort events chronologically within each patient case
df = df.sort_values(
    ["case:concept:name", "time:timestamp"]
).reset_index(drop=True)

event_log = pm4py.convert_to_event_log(df)

print(f"Total cases: {len(event_log)}")


# --------------------------------------------------
# 2. Build ideal clinical process
# --------------------------------------------------

registration = ProcessTree(label="Registration")
triage = ProcessTree(label="Triage")
doctor = ProcessTree(label="Doctor")
discharge = ProcessTree(label="Discharge")

ideal_process = ProcessTree(
    operator=Operator.SEQUENCE,
    children=[
        registration,
        triage,
        doctor,
        discharge
    ]
)

print("Ideal process:")
print(ideal_process)


# --------------------------------------------------
# 3. Convert ideal process to Petri net
# --------------------------------------------------

net, initial_marking, final_marking = pm4py.convert_to_petri_net(
    ideal_process
)

print("Ideal Petri net created.")


# --------------------------------------------------
# 4. Run token-based replay
# --------------------------------------------------

replayed_traces = token_replay.apply(
    event_log,
    net,
    initial_marking,
    final_marking
)

print(
    f"Conformance checking completed for "
    f"{len(replayed_traces)} cases."
)


# --------------------------------------------------
# 5. Calculate conformance metrics
# --------------------------------------------------

total_cases = len(replayed_traces)

conforming_cases = sum(
    result["trace_is_fit"]
    for result in replayed_traces
)

non_conforming_cases = total_cases - conforming_cases

conformance_rate = (
    conforming_cases / total_cases
) * 100

average_fitness = sum(
    result["trace_fitness"]
    for result in replayed_traces
) / total_cases

cases_with_missing_tokens = sum(
    result["missing_tokens"] > 0
    for result in replayed_traces
)

# Fitness comparison
conforming_fitness = [
    result["trace_fitness"]
    for result in replayed_traces
    if result["trace_is_fit"]
]

non_conforming_fitness = [
    result["trace_fitness"]
    for result in replayed_traces
    if not result["trace_is_fit"]
]

average_conforming_fitness = (
    sum(conforming_fitness) / len(conforming_fitness)
    if conforming_fitness
    else 0
)

average_non_conforming_fitness = (
    sum(non_conforming_fitness) / len(non_conforming_fitness)
    if non_conforming_fitness
    else 0
)


# --------------------------------------------------
# 6. Display results
# --------------------------------------------------

print("\n" + "=" * 50)
print("CONFORMANCE RESULTS")
print("=" * 50)

print(f"Total cases:               {total_cases}")
print(f"Conforming cases:          {conforming_cases}")
print(f"Non-conforming cases:      {non_conforming_cases}")
print(f"Conformance rate:          {conformance_rate:.2f}%")
print(f"Average trace fitness:     {average_fitness:.4f}")
print(f"Conforming avg fitness:    {average_conforming_fitness:.4f}")
print(f"Non-conforming avg fitness:{average_non_conforming_fitness:.4f}")
print(
    f"Cases with missing tokens: {cases_with_missing_tokens}"
)

print("=" * 50)

# ==================================================
# DEVIATION ANALYSIS
# ==================================================

# Sort events chronologically within each case
sorted_df = df.sort_values(
    ["case:concept:name", "time:timestamp"]
).reset_index(drop=True)

# Build chronological activity sequence for each case
case_sequences = (
    sorted_df.groupby("case:concept:name")["concept:name"]
    .apply(list)
)

# Identify cases containing the X-Ray loop-back
loopback_sequence = [
    "Registration",
    "Triage",
    "Doctor",
    "X-Ray",
    "Triage",
    "Doctor",
    "Discharge",
]

loopback_cases = case_sequences[
    case_sequences.apply(lambda x: x == loopback_sequence)
]

print("\n==================================================")
print("DEVIATION ANALYSIS")
print("==================================================")
print(f"X-Ray loop-back cases:     {len(loopback_cases)}")
print(f"Percentage of all cases:   {len(loopback_cases) / len(case_sequences) * 100:.2f}%")
print("Deviation pattern:")
print("Registration -> Triage -> Doctor -> X-Ray")
print("-> Triage -> Doctor -> Discharge")
print("==================================================")
