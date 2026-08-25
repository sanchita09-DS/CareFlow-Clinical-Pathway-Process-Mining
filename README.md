# CareFlow

CareFlow is a clinical pathway process mining project.

## Team

- Person 1 - Team Leader + Integration
- Person 2
- Person 3
- Person 4

## Project Structure

- `docs/` - Project documentation
- `src/` - Python/source code
- `data/` - Dataset and processed data
- `sql/` - SQL queries
- `dbt/` - dbt models and transformations
- `tests/` - Data and pipeline tests

## Python Event Generator (Alam)

Generates simulated hospital patient event logs for process mining analysis.

### What it does
- Simulates 300 patients moving through hospital activities
- Each patient follows either a **normal path** (Registration → Triage → Doctor → Discharge)
  or an **inefficient path** with a loop-back (Registration → Triage → Doctor → X-Ray → Triage → Doctor → Discharge)
- Attaches realistic, chronologically ordered timestamps to every event
- Validates the generated data (no missing fields, no out-of-order timestamps)
- Exports the dataset to CSV for loading into BigQuery

### How to run it
```bash
cd src/data_generator
python patient_generator.py
```

This will:
1. Generate 300 patients (~1,400 events)
2. Print a sample of the first 10 events
3. Show the normal/inefficient path distribution
4. Run validation checks
5. Export the data to `data/samples/patient_events.csv`

### Files
| File | Purpose |
|---|---|
| `src/data_generator/activities.py` | Activity list and path templates (normal/inefficient) |
| `src/data_generator/patient_generator.py` | Core generation, timestamping, validation, CSV export |
| `data/samples/patient_events.csv` | Sample generated dataset (300 patients, ~1,400 events) |

---

## BigQuery Setup (Alam)

### Dataset & Table
- **Project:** `project-8aac59b5-de99-438d-ad8`
- **Dataset:** `careflow_raw`
- **Table:** `patient_events_raw`
- **Location:** us-central1

### Schema
See [`docs/event_log_schema.md`](docs/event_log_schema.md) for the full schema definition.

### How to load new data
1. Run the generator (see above) to produce `data/samples/patient_events.csv`
2. In BigQuery Studio, open `careflow_raw.patient_events_raw`
3. Click **+** → **Upload** → select the CSV
4. Set **Header rows to skip = 1**, **Write preference = Append to table**
5. Click **Create table**

### Validation queries
See [`sql/bigquery/validation_queries.sql`](sql/bigquery/validation_queries.sql) for queries to check row counts, spot-check a patient's journey, and confirm no NULL values.

**Current dataset status:** 300 patients, 1,404 events, fully validated (no NULLs, chronological order confirmed).

## dbt Transformation (Sachita)

### Project
- **Dataset:** `careflow_dbt_uscentral1`
- **Staging model:** `stg_patient_events`

### What it does
Takes the raw event data from `careflow_raw.patient_events_raw` and produces a clean staging view (`stg_patient_events`) ready for Week 2's process mining analysis.

### How to run it
```bash
cd dbt/careflow_dbt
dbt run
```

### Validation
```sql
SELECT COUNT(*) FROM `project-8aac59b5-de99-438d-ad8.careflow_dbt_uscentral1.stg_patient_events`;
```
**Result:** 1,404 rows — exact match with the raw table, confirming no data loss through the pipeline.
