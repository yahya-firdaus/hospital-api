from app.models import db, Employee
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound, BadRequest
from ..services.auth_service import hash_password

def get_all_employees():
    return Employee.query.all()

def get_employee_by_id(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        raise NotFound("Employee not found")
    return employee

def create_employee(data):
    try:
        new_employee = Employee(
            name=data.get('name'),
            username=data.get('username'),
            password=hash_password(data.get('password')),
            gender=data.get('gender'),
            birthdate=data.get('birthdate')
        )
        db.session.add(new_employee)
        db.session.commit()
        return new_employee
    except IntegrityError:
        db.session.rollback()
        raise BadRequest("Username already exists")

def update_employee(employee_id, data):
    employee = Employee.query.get(employee_id)
    if not employee:
        raise NotFound("Employee not found")

    employee.name = data.get('name')
    employee.username = data.get('username')
    employee.password = hash_password(data.get('password'))
    employee.gender = data.get('gender')
    employee.birthdate = data.get('birthdate')

    db.session.commit()
    return employee

def delete_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        raise NotFound("Employee not found")

    db.session.delete(employee)
    db.session.commit()
