import pm4py
from pm4py.objects.process_tree.obj import ProcessTree, Operator


# Define the ideal clinical process
# Registration -> Triage -> Doctor -> Discharge

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

# Convert Process Tree to Petri Net
net, initial_marking, final_marking = pm4py.convert_to_petri_net(
    ideal_process
)

# Save the ideal model
pm4py.write_pnml(
    net,
    initial_marking,
    final_marking,
    "data/samples/ideal_careflow_model.pnml"
)

print("Ideal process created successfully.")
print("Process: Registration -> Triage -> Doctor -> Discharge")
print("Saved: data/samples/ideal_careflow_model.pnml")
