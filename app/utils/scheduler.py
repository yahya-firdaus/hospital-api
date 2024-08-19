from google.cloud import bigquery
from google.oauth2 import service_account
from app import db
from app.models import Patient
from datetime import datetime
import pytz
from apscheduler.triggers.interval import IntervalTrigger
from app.utils.bigquery import update_patients_from_bigquery

# Function for get data from BigQuery and update database
def update_patients_from_bigquery():
    credentials = service_account.Credentials.from_service_account_file(
        'app/utils/bigquery_credentials.json'
    )

    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    query = """
    SELECT no_ktp, vaccine_type, vaccine_count
    FROM `delman-internal.delman_interview.vaccine_data`
    """

    query_job = client.query(query)
    results = query_job.result()

    for row in results:
        patient = Patient.query.filter_by(no_ktp=row.no_ktp).first()
        if patient:
            patient.vaccine_type = row.vaccine_type
            patient.vaccine_count = row.vaccine_count
            patient.updated_at = datetime.now(pytz.utc)

    db.session.commit()

def schedule_updates(scheduler):
    # scheduler.add_job(update_patients_from_bigquery, 'interval', hours=24)
    scheduler.add_job(
        func=update_patients_from_bigquery,
        trigger=IntervalTrigger(hours=24),
        id='update_patients_job',
        name='Update patients from BigQuery every 24 hours',
        replace_existing=True
    )

# def update_patients_from_bigquery():
#     client = bigquery.Client()
#     query = "SELECT * FROM `delman-internal.delman_interview.vaccine_data`"
#     results = client.query(query).result()
    
#     for row in results:
#         patient = Patient.query.filter_by(no_ktp=row.no_ktp).first()
#         if patient:
#             patient.vaccine_type = row.vaccine_type
#             patient.vaccine_count = row.vaccine_count
#         else:
#             patient = Patient(
#                 name=row.name,
#                 gender=row.gender,
#                 birthdate=row.birthdate,
#                 no_ktp=row.no_ktp,
#                 address=row.address,
#                 vaccine_type=row.vaccine_type,
#                 vaccine_count=row.vaccine_count
#             )
#             db.session.add(patient)
    
#     db.session.commit()
