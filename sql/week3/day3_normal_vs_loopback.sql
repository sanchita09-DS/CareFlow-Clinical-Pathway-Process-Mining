WITH case_duration AS (
  SELECT
    case_id,
    TIMESTAMP_DIFF(
      MAX(event_timestamp),
      MIN(event_timestamp),
      MINUTE
    ) AS total_duration_minutes
  FROM `project-8aac59b5-de99-438d-ad8.careflow_dbt_uscentral1.stg_patient_events`
  GROUP BY case_id
),

case_types AS (
  SELECT
    case_id,
    COUNTIF(activity_name = 'Triage') AS triage_count
  FROM `project-8aac59b5-de99-438d-ad8.careflow_dbt_uscentral1.stg_patient_events`
  GROUP BY case_id
)

SELECT
  CASE
    WHEN ct.triage_count > 1 THEN 'Loop-back'
    ELSE 'Normal'
  END AS pathway_type,

  COUNT(*) AS patient_count,

  ROUND(AVG(cd.total_duration_minutes), 2) AS avg_duration_minutes,

  APPROX_QUANTILES(cd.total_duration_minutes, 2)[OFFSET(1)]
    AS median_duration_minutes

FROM case_duration cd
JOIN case_types ct
  ON cd.case_id = ct.case_id

GROUP BY pathway_type
ORDER BY pathway_type;

