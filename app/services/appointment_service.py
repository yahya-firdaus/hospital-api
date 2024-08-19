from app.models import db, Appointment

def get_all_appointments():
    return [appointment.to_dict() for appointment in Appointment.query.all()]

def get_appointment_by_id(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        raise ValueError("Appointment not found")
    return appointment.to_dict()

def create_appointment(data):
    new_appointment = Appointment(**data)
    db.session.add(new_appointment)
    db.session.commit()
    return new_appointment.to_dict()

def update_appointment(appointment_id, data):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        raise ValueError("Appointment not found")
    for key, value in data.items():
        setattr(appointment, key, value)
    db.session.commit()
    return appointment.to_dict()

def delete_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        raise ValueError("Appointment not found")
    db.session.delete(appointment)
    db.session.commit()
