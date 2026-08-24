SELECT
    Case_ID,
    Activity_Name,
    Timestamp
FROM {{ source('careflow_raw', 'patient_events_raw') }}