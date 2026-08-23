# CareFlow Event Log Schema — BigQuery

**Dataset:** `careflow_raw`
**Table:** `patient_events_raw`
**Location:** us-central1

| Column | Type | Description |
|---|---|---|
| Case_ID | STRING | Unique patient case identifier (e.g. P001) |
| Activity_Name | STRING | Hospital activity (Registration, Triage, Doctor, X-Ray, Pharmacy, Discharge) |
| Timestamp | TIMESTAMP | When the activity occurred |