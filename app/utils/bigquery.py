from google.cloud import bigquery
import os

# Set environment variable for Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"

def update_patients_from_bigquery():
    # Create a BigQuery client
    client = bigquery.Client()

    # Define BigQuery SQL query
    query = """
    SELECT
        no_ktp,
        name,
        birthdate,
        gender
    FROM
        `delman-internal.delman_interview.vaccine_data`
    """

    # Run the query and get the results
    query_job = client.query(query)
    results = query_job.result()

    # Process the results
    for row in results:
        # In Progress ...
        print(f"no_ktp: {row.no_ktp}, name: {row.name}, birthdate: {row.birthdate}, gender: {row.gender}")

