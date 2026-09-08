# CareFlow — Week 1 Review

## Summary
Week 1's goal was to prove the team could reliably generate, store, and clean patient event data. **This is confirmed working end-to-end.**

## Pipeline Verified
```Python Generator → BigQuery Raw Table → dbt Staging Model
1,404 events → 1,404 rows → 1,404 rows

## What Was Built
- **Python event simulator** — generates 300 realistic patient journeys (normal + inefficient/loop-back paths), with chronological timestamps and validation checks
- **BigQuery data warehouse** — `careflow_raw.patient_events_raw` table storing the full dataset
- **dbt staging layer** — `careflow_dbt_uscentral1.stg_patient_events`, cleaned and ready for Week 2

## Data Quality Results
- 300 unique patients, 1,404 total events
- No NULL values in Case_ID, Activity_Name, or Timestamp
- All timestamps confirmed in chronological order per patient
- ~77-81% normal paths, ~19-23% inefficient (loop-back) paths — consistent with the intended 80/20 design

## Known Issues (Resolved)
- `main` branch briefly lost its commit history mid-week due to an accidental nested-`.git` issue during dbt setup. Recovered fully using `git merge --allow-unrelated-histories`, with one manual conflict resolution in `patient_generator.py`. No data was lost.
- An empty duplicate dbt dataset (`careflow_dbt`) was created and has been cleaned up — `careflow_dbt_uscentral1` is the dataset in active use.

## Week 2 Plan
- Event log normalization
- PM4Py process discovery on `stg_patient_events`
- Begin identifying bottlenecks and loop-back patterns in the discovered process map