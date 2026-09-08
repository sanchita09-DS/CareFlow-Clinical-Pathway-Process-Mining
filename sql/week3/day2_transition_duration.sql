WITH ordered_events AS (

  SELECT
    case_id,
    activity_name,
    event_timestamp,
    LEAD(activity_name) OVER (
      PARTITION BY case_id
      ORDER BY event_timestamp
    ) AS next_activity,
    LEAD(event_timestamp) OVER (
      PARTITION BY case_id
      ORDER BY event_timestamp
    ) AS next_timestamp
  FROM `project-8aac59b5-de99-438d-ad8.careflow_dbt_uscentral1.stg_patient_events`
)

SELECT
  activity_name AS from_activity,
  next_activity AS to_activity,
  ROUND(
    AVG(
      TIMESTAMP_DIFF(next_timestamp, event_timestamp, MINUTE)
    ),
    1
  ) AS avg_minutes,
  COUNT(*) AS transition_count
FROM ordered_events
WHERE next_activity IS NOT NULL
GROUP BY from_activity, next_activity
ORDER BY avg_minutes DESC;

