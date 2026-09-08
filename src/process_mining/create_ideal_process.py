import pm4py

from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils import petri_utils


# --------------------------------------------------
# Create ideal clinical process Petri net
# Registration -> Triage -> Doctor -> Discharge
# --------------------------------------------------

net = PetriNet("CareFlow Ideal Process")

# Places
p_start = PetriNet.Place("start")
p_registration = PetriNet.Place("registration")
p_triage = PetriNet.Place("triage")
p_doctor = PetriNet.Place("doctor")
p_discharge = PetriNet.Place("discharge")
p_end = PetriNet.Place("end")

net.places.add(p_start)
net.places.add(p_registration)
net.places.add(p_triage)
net.places.add(p_doctor)
net.places.add(p_discharge)
net.places.add(p_end)


# Transitions
t_registration = PetriNet.Transition(
    "registration_transition",
    "Registration"
)

t_triage = PetriNet.Transition(
    "triage_transition",
    "Triage"
)

t_doctor = PetriNet.Transition(
    "doctor_transition",
    "Doctor"
)

t_discharge = PetriNet.Transition(
    "discharge_transition",
    "Discharge"
)

net.transitions.add(t_registration)
net.transitions.add(t_triage)
net.transitions.add(t_doctor)
net.transitions.add(t_discharge)


# Connect places and transitions
petri_utils.add_arc_from_to(
    p_start,
    t_registration,
    net
)

petri_utils.add_arc_from_to(
    t_registration,
    p_registration,
    net
)

petri_utils.add_arc_from_to(
    p_registration,
    t_triage,
    net
)

petri_utils.add_arc_from_to(
    t_triage,
    p_triage,
    net
)

petri_utils.add_arc_from_to(
    p_triage,
    t_doctor,
    net
)

petri_utils.add_arc_from_to(
    t_doctor,
    p_doctor,
    net
)

petri_utils.add_arc_from_to(
    p_doctor,
    t_discharge,
    net
)

petri_utils.add_arc_from_to(
    t_discharge,
    p_end,
    net
)


# Initial and final markings
initial_marking = Marking()
initial_marking[p_start] = 1

final_marking = Marking()
final_marking[p_end] = 1


# Save model
pm4py.write_pnml(
    net,
    initial_marking,
    final_marking,
    "data/samples/ideal_careflow_model.pnml"
)

print("Ideal Petri net created successfully.")
print("Process: Registration -> Triage -> Doctor -> Discharge")
print("Saved: data/samples/ideal_careflow_model.pnml")
