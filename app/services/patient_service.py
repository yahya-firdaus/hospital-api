from app.models import db, Patient
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound, BadRequest

def get_all_patients():
    return Patient.query.all()

def get_patient_by_id(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        raise NotFound("Patient not found")
    return patient

def create_patient(data):
    try:
        new_patient = Patient(
            name=data.get('name'),
            gender=data.get('gender'),
            birthdate=data.get('birthdate'),
            no_ktp=data.get('no_ktp'),
            address=data.get('address')
        )
        db.session.add(new_patient)
        db.session.commit()
        return new_patient
    except IntegrityError:
        db.session.rollback()
        raise BadRequest("Patient with this KTP already exists")

def update_patient(patient_id, data):
    patient = Patient.query.get(patient_id)
    if not patient:
        raise NotFound("Patient not found")

    patient.name = data.get('name')
    patient.gender = data.get('gender')
    patient.birthdate = data.get('birthdate')
    patient.no_ktp = data.get('no_ktp')
    patient.address = data.get('address')

    db.session.commit()
    return patient

def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        raise NotFound("Patient not found")

    db.session.delete(patient)
    db.session.commit()
