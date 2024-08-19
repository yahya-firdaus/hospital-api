from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.employee_service import get_all_employees, get_employee_by_id, create_employee, update_employee, delete_employee
from app.requests.employee_request import validate_employee_data
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import BadRequest, NotFound

bp = Blueprint('employees', __name__, url_prefix='/employees')

ns = Namespace('employees', description='Employee management operations')

employee_model = ns.model('Employee', {
    'name': fields.String(required=True, description='Name of the employee'),
    'username': fields.String(required=True, description='Username of the employee'),
    'password': fields.String(required=True, description='Password of the employee'),
    'gender': fields.String(description='Gender of the employee'),
    'birthdate': fields.String(description='Birthdate of the employee (YYYY-MM-DD)')
})

@ns.route('/')
class EmployeesResource(Resource):
    @jwt_required()
    def get(self):
        employees = get_all_employees()
        return jsonify([employee.as_dict() for employee in employees])

    @ns.expect(employee_model, validate=True)
    @jwt_required()
    def post(self):
        data = request.get_json()
        errors = validate_employee_data(data)
        if errors:
            return jsonify({"errors": errors})
        try:
            employee = create_employee(data)
            return jsonify(employee.as_dict())
        except BadRequest as e:
            return jsonify({"error": str(e)})

@ns.route('/<int:id>')
class EmployeeResource(Resource):
    @jwt_required()
    def get(self, id):
        try:
            employee = get_employee_by_id(id)
            return jsonify(employee.as_dict())
        except NotFound as e:
            return jsonify({"error": str(e)})

    @ns.expect(employee_model, validate=True)
    @jwt_required()
    def put(self, id):
        data = request.get_json()
        errors = validate_employee_data(data)
        if errors:
            return jsonify({"errors": errors})
        try:
            employee = update_employee(id, data)
            return jsonify(employee.as_dict())
        except NotFound as e:
            return jsonify({"error": str(e)})

    @jwt_required()
    def delete(self, id):
        try:
            delete_employee(id)
            return jsonify({"message": "deleted successfully"})
        except NotFound as e:
            return jsonify({"error": str(e)})
