from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.String(16), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'gender': self.gender,
            'birthdate': self.birthdate.isoformat()
        }

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.String(16), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    work_start_time = db.Column(db.Time, nullable=False)
    work_end_time = db.Column(db.Time, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_available(self, appointment_time: datetime):
        # Logika untuk memeriksa ketersediaan dokter
        work_start_time = datetime.combine(appointment_time.date(), self.work_start_time)
        work_end_time = datetime.combine(appointment_time.date(), self.work_end_time)
        
        return work_start_time <= appointment_time <= work_end_time

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'gender': self.gender,
            'birthdate': self.birthdate.isoformat(),
            'work_start_time': str(self.work_start_time),
            'work_end_time': str(self.work_end_time)
        }

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.String(16), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    no_ktp = db.Column(db.String(16), unique=True, nullable=False)
    address = db.Column(db.String(256), nullable=False)
    vaccine_type = db.Column(db.String(128))
    vaccine_count = db.Column(db.Integer)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'birthdate': self.birthdate.isoformat(),
            'no_ktp': self.no_ktp,
            'address': self.address,
            'vaccine_type': self.vaccine_type,
            'vaccine_count': self.vaccine_count
        }

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(16), nullable=False)
    diagnose = db.Column(db.Text, default="")
    notes = db.Column(db.Text, default="")

    def as_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'datetime': self.datetime.isoformat(),
            'status': self.status,
            'diagnose': self.diagnose,
            'notes': self.notes
        }
