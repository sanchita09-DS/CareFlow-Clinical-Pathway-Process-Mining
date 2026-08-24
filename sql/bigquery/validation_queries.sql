-- CareFlow Week 1 — BigQuery Validation Queries

-- 1. Total row count and unique patient count
SELECT COUNT(DISTINCT Case_ID) AS total_patients, COUNT(*) AS total_events
FROM `project-8aac59b5-de99-438d-ad8.careflow_raw.patient_events_raw`;
-- Expected: 300 patients, ~1300-1500 events

-- 2. View one patient's full journey, in order
SELECT * FROM `project-8aac59b5-de99-438d-ad8.careflow_raw.patient_events_raw`
WHERE Case_ID = 'P001'
ORDER BY Timestamp;

-- 3. Check for any NULL values (should return 0 rows)
SELECT * FROM `project-8aac59b5-de99-438d-ad8.careflow_raw.patient_events_raw`
WHERE Case_ID IS NULL OR Activity_Name IS NULL OR Timestamp IS NULL;