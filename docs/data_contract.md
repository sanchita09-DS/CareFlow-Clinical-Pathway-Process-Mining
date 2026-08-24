# CareFlow Week 1 Data Contract

## Purpose

This document defines the agreed structure and rules for the CareFlow
healthcare event log.

The data contract is shared between the Python event generator,
BigQuery raw table, and dbt transformation layer.

## Event Log Schema

| Column | Data Type | Description |
|---|---|---|
| Case_ID | STRING | Unique identifier for a clinical case/process instance |
| Activity_Name | STRING | Name of the activity/event performed |
| Timestamp | TIMESTAMP | Date and time at which the activity occurred |

## Approved Activities

The planned CareFlow activity list is:

- Registration
- Triage
- Doctor
- Blood Test
- X-Ray
- Pharmacy
- Discharge

> Note: The current sample event log contains Registration, Triage,
> Doctor, X-Ray, and Discharge. Blood Test and Pharmacy are part of
> the approved activity list but are not currently present in the
> inspected sample.

## Rules

1. Case_ID must not be empty.
2. Activity_Name must not be empty.
3. Timestamp must not be empty.
4. Timestamp must represent the event time.
5. Activities belonging to the same case must use the same Case_ID.
6. Activity names must follow the approved activity naming list.
7. Timestamps must use a consistent format.
8. Events belonging to the same case should be ordered chronologically.

## Timestamp Rules

- Timestamp must contain both date and time.
- Timestamp values use the format `YYYY-MM-DD HH:MM:SS`.
- Example: `2026-08-01 09:44:00`.
- Timestamp cannot be empty.
- All timestamps must use the same format.
- Events belonging to the same case should be ordered chronologically.

## Example

| Case_ID | Activity_Name | Timestamp |
|---|---|---|
| P001 | Registration | 2026-08-01 09:44:00 |
| P001 | Triage | 2026-08-01 10:16:00 |
| P001 | Doctor | 2026-08-01 10:41:00 |
| P001 | Discharge | 2026-08-01 11:09:00 |