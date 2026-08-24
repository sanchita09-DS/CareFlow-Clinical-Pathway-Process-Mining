SELECT
    Case_ID AS case_id,
    Activity_Name AS activity_name,
    Timestamp AS event_timestamp
FROM {{ source('careflow_raw', 'patient_events_raw') }}