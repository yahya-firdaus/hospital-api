from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.appointment_service import (
    get_all_appointments,
    get_appointment_by_id,
    create_appointment,
    update_appointment,
    delete_appointment,
)
from app.requests.appointment_request import validate_appointment_request
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import BadRequest, NotFound

bp = Blueprint('appointments', __name__)

ns = Namespace('appointments', description='Appointment management operations')

appointment_model = ns.model('Appointment', {
    'patient_id': fields.Integer(required=True, description='ID of the patient'),
    'doctor_id': fields.Integer(required=True, description='ID of the doctor'),
    'datetime': fields.String(required=True, description='Appointment date and time (YYYY-MM-DD HH:MM)'),
    'status': fields.String(description='Status of the appointment (IN_QUEUE, DONE, CANCELLED)'),
    'diagnose': fields.String(description='Diagnosis made during the appointment'),
    'notes': fields.String(description='Additional notes about the appointment')
})

@ns.route('/')
class AppointmentsResource(Resource):
    @jwt_required()
    def get(self):
        try:
            appointments = get_all_appointments()
            return jsonify(appointments)
        except Exception as e:
            return jsonify({'error': str(e)})

    @ns.expect(appointment_model, validate=True)
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            validate_appointment_request(data)
            appointment = create_appointment(data)
            return jsonify(appointment)
        except Exception as e:
            return jsonify({'error': str(e)})

@ns.route('/<int:id>')
class AppointmentResource(Resource):
    @jwt_required()
    def get(self, id):
        try:
            appointment = get_appointment_by_id(id)
            return jsonify(appointment)
        except Exception as e:
            return jsonify({'error': str(e)})

    @ns.expect(appointment_model, validate=True)
    @jwt_required()
    def put(self, id):
        try:
            data = request.get_json()
            validate_appointment_request(data)
            appointment = update_appointment(id, data)
            return jsonify(appointment)
        except Exception as e:
            return jsonify({'error': str(e)})

    @jwt_required()
    def delete(self, id):
        try:
            delete_appointment(id)
            return jsonify({'message': 'Appointment deleted successfully'})
        except Exception as e:
            return jsonify({'error': str(e)})
