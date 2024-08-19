# Validation when create data
def validate_appointment_request(data):
    required_fields = ['patient_id', 'doctor_id', 'datetime', 'status']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
