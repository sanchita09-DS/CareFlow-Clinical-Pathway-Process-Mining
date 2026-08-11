# CareFlow Week 1 Data Contract

## Event Log Schema

The CareFlow event log will contain the following fields:

| Column | Data Type | Description |
|---|---|---|
| Case_ID | STRING | Unique identifier for a clinical case/process instance |
| Activity_Name | STRING | Name of the activity/event performed |
| Timestamp | DATETIME | Date and time at which the activity occurred |

## Rules

1. Case_ID must not be empty.
2. Activity_Name must not be empty.
3. Timestamp must not be empty.
4. Timestamp must represent the actual event time.
5. Activities belonging to the same case must use the same Case_ID.
6. Activity names must follow the approved activity naming list.
7. Timestamp must use a consistent date-time format.

## Example

| Case_ID | Activity_Name | Timestamp |
|---|---|---|
| C001 | Registration | 2026-01-10 09:30:00 |
| C001 | Diagnosis | 2026-01-10 10:15:00 |
| C001 | Lab_Test | 2026-01-10 11:30:00 |



## Timestamp Rules

- Timestamp must contain both date and time.
- Timestamp must use the format YYYY-MM-DD HH:MM:SS.
- Timestamp cannot be empty.
- All timestamps must use the same format.
- Events belonging to a case should be ordered chronologically.
- example 2026-01-10 09:30:00
