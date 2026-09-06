SELECT
  case_id,
  MIN(event_timestamp) AS journey_start,
  MAX(event_timestamp) AS journey_end,
  TIMESTAMP_DIFF(
    MAX(event_timestamp),
    MIN(event_timestamp),
    MINUTE
  ) AS total_duration_minutes
FROM `project-8aac59b5-de99-438d-ad8.careflow_dbt_uscentral1.stg_patient_events`
GROUP BY case_id
ORDER BY total_duration_minutes DESC;

