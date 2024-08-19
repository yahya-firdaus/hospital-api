# Validation when create data employee
def validate_employee_data(data):
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
    return errors
