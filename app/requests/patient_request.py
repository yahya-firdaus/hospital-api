# Validation when create data patient
def validate_patient_data(data):
    errors = {}
    if 'name' not in data:
        errors['name'] = 'Name is required'
    if 'gender' not in data:
        errors['gender'] = 'Gender is required'
    if 'birthdate' not in data:
        errors['birthdate'] = 'Birthdate is required'
    if 'no_ktp' not in data:
        errors['no_ktp'] = 'No KTP is required'
    if 'address' not in data:
        errors['address'] = 'Address is required'
    return errors
