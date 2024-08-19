from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.doctor_service import get_all_doctors, get_doctor_by_id, create_doctor, update_doctor, delete_doctor
from app.requests.doctor_request import validate_doctor_data
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import BadRequest, NotFound

bp = Blueprint('doctors', __name__, url_prefix='/doctors')

ns = Namespace('doctors', description='Doctor management operations')

doctor_model = ns.model('Doctor', {
    'name': fields.String(required=True, description='Name of the doctor'),
    'username': fields.String(required=True, description='Username of the doctor'),
    'password': fields.String(required=True, description='Password of the doctor'),
    'gender': fields.String(description='Gender of the doctor'),
    'birthdate': fields.String(description='Birthdate of the doctor (YYYY-MM-DD)'),
    'work_start_time': fields.String(description='Doctor work start time (HH:MM)'),
    'work_end_time': fields.String(description='Doctor work end time (HH:MM)')
})

@ns.route('/')
class DoctorsResource(Resource):
    @jwt_required()
    def get(self):
        doctors = get_all_doctors()
        return jsonify([doctor.as_dict() for doctor in doctors])

    @ns.expect(doctor_model, validate=True)
    @jwt_required()
    def post(self):
        data = request.get_json()
        errors = validate_doctor_data(data)
        if errors:
            return jsonify({"errors": errors})
        try:
            doctor = create_doctor(data)
            return jsonify(doctor.as_dict())
        except BadRequest as e:
            return jsonify({"error": str(e)})

@ns.route('/<int:id>')
class DoctorResource(Resource):
    @jwt_required()
    def get(self, id):
        try:
            doctor = get_doctor_by_id(id)
            return jsonify(doctor.as_dict())
        except NotFound as e:
            return jsonify({"error": str(e)})

    @ns.expect(doctor_model, validate=True)
    @jwt_required()
    def put(self, id):
        data = request.get_json()
        errors = validate_doctor_data(data)
        if errors:
            return jsonify({"errors": errors})
        try:
            doctor = update_doctor(id, data)
            return jsonify(doctor.as_dict())
        except NotFound as e:
            return jsonify({"error": str(e)})

    @jwt_required()
    def delete(self, id):
        try:
            delete_doctor(id)
            return jsonify({"message": "deleted successfully"})
        except NotFound as e:
            return jsonify({"error": str(e)})
