from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.patient_service import get_all_patients, get_patient_by_id, create_patient, update_patient, delete_patient
from app.requests.patient_request import validate_patient_data
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import BadRequest, NotFound

bp = Blueprint('patients', __name__, url_prefix='/patients')

ns = Namespace('patients', description='Patient management operations')

patient_model = ns.model('Patient', {
    'name': fields.String(required=True, description='Name of the patient'),
    'gender': fields.String(description='Gender of the patient'),
    'birthdate': fields.String(description='Birthdate of the patient (YYYY-MM-DD)'),
    'no_ktp': fields.String(required=True, description='National ID number of the patient'),
    'address': fields.String(description='Address of the patient'),
    'vaccine_type': fields.String(description='Type of vaccine received by the patient'),
    'vaccine_count': fields.Integer(description='Number of vaccine doses received by the patient')
})

@ns.route('/')
class PatientsResource(Resource):
    @jwt_required()
    def get(self):
        patients = get_all_patients()
        return jsonify([patient.as_dict() for patient in patients])

    @ns.expect(patient_model, validate=True)
    @jwt_required()
    def post(self):
        data = request.get_json()
        errors = validate_patient_data(data)
        if errors:
            return jsonify({"errors": errors})
        try:
            patient = create_patient(data)
            return jsonify(patient.as_dict())
        except BadRequest as e:
            return jsonify({"error": str(e)})

@ns.route('/<int:id>')
class PatientResource(Resource):
    @jwt_required()
    def get(self, id):
        try:
            patient = get_patient_by_id(id)
            return jsonify(patient.as_dict())
        except NotFound as e:
            return jsonify({"error": str(e)})

    @ns.expect(patient_model, validate=True)
    @jwt_required()
    def put(self, id):
        data = request.get_json()
        errors = validate_patient_data(data)
        if errors:
            return jsonify({"errors": errors})
        try:
            patient = update_patient(id, data)
            return jsonify(patient.as_dict())
        except NotFound as e:
            return jsonify({"error": str(e)})

    @jwt_required()
    def delete(self, id):
        try:
            delete_patient(id)
            return jsonify({"message": "deleted successfully"})
        except NotFound as e:
            return jsonify({"error": str(e)})
