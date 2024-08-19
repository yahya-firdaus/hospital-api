from app.models import db, Doctor
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound, BadRequest
from ..services.auth_service import hash_password

def get_all_doctors():
    return Doctor.query.all()

def get_doctor_by_id(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        raise NotFound("Doctor not found")
    return doctor

def create_doctor(data):
    try:
        new_doctor = Doctor(
            name=data.get('name'),
            username=data.get('username'),
            password=hash_password(data.get('password')),
            gender=data.get('gender'),
            birthdate=data.get('birthdate'),
            work_start_time=data.get('work_start_time'),
            work_end_time=data.get('work_end_time')
        )
        db.session.add(new_doctor)
        db.session.commit()
        return new_doctor
    except IntegrityError:
        db.session.rollback()
        raise BadRequest("Username already exists")

def update_doctor(doctor_id, data):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        raise NotFound("Doctor not found")

    doctor.name = data.get('name')
    doctor.username = data.get('username')
    doctor.password = hash_password(data.get('password'))
    doctor.gender = data.get('gender')
    doctor.birthdate = data.get('birthdate')
    doctor.work_start_time = data.get('work_start_time')
    doctor.work_end_time = data.get('work_end_time')

    db.session.commit()
    return doctor

def delete_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        raise NotFound("Doctor not found")

    db.session.delete(doctor)
    db.session.commit()
