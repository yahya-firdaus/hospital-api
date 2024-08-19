# Validation when create data doctor
def validate_doctor_data(data):
    errors = {}
    if 'name' not in data:
        errors['name'] = 'Name is required'
    if 'username' not in data:
        errors['username'] = 'Username is required'
    if 'password' not in data:
        errors['password'] = 'Password is required'
    if 'gender' not in data:
        errors['gender'] = 'Gender is required'
    if 'birthdate' not in data:
        errors['birthdate'] = 'Birthdate is required'
    if 'work_start_time' not in data:
        errors['work_start_time'] = 'Work start time is required'
    if 'work_end_time' not in data:
        errors['work_end_time'] = 'Work end time is required'
    return errors
