from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required
from ..services.auth_service import hash_password, check_password
from ..models import Employee
from .. import db

bp = Blueprint('auth', __name__)

ns = Namespace('auth', description='Authentication operations')

login_model = ns.model('Login', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='The password')
})

@ns.route('/login')
class LoginResource(Resource):
    @ns.expect(login_model, validate=True)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        employee = Employee.query.filter_by(username=username).first()

        if not employee or not check_password(employee.password, password):
            return {"message": "Invalid username or password"}, 401

        access_token = create_access_token(identity={'username': username})
        return {"access_token": access_token}, 200
