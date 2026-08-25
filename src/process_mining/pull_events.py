from google.cloud import bigquery

PROJECT_ID = "project-8aac59b5-de99-438d-ad8"
TABLE = "careflow_dbt_uscentral1.stg_patient_events"

client = bigquery.Client(project=PROJECT_ID)

query = f"""
    SELECT case_id, activity_name, event_timestamp
    FROM `{PROJECT_ID}.{TABLE}`
"""

df = client.query(query).to_dataframe()

print("Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
df.to_csv("data/samples/stg_patient_events.csv", index=False)
print("Saved to data/samples/stg_patient_events.csv")