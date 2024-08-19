from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError
from werkzeug.exceptions import HTTPException
from flask_apscheduler import APScheduler
from .config import Config
from .swagger.swagger_config import initialize_swagger

db = SQLAlchemy()
# jwt = JWTManager()
scheduler = APScheduler()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    jwt = JWTManager(app)

    db.init_app(app)
    jwt.init_app(app)
    scheduler.init_app(app)

    # Initialize Swagger
    initialize_swagger(app)

    app.config['JWT_SECRET_KEY'] = 'your-secret-key'

    # Error handler for NoAuthorizationError
    @app.errorhandler(NoAuthorizationError)
    def handle_no_authorization_error(e):
        return jsonify({"message": "Missing or invalid Authorization Header"}), 401

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return jsonify({"message": e.description}), e.code
        return jsonify({"message": "An unexpected error occurred"}), 500

    # Register Blueprints
    from .routes.auth import bp as auth_bp
    from .routes.employees import bp as employees_bp
    from .routes.doctors import bp as doctors_bp
    from .routes.patients import bp as patients_bp
    from .routes.appointments import bp as appointments_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(employees_bp, url_prefix='/employees')
    app.register_blueprint(doctors_bp, url_prefix='/doctors')
    app.register_blueprint(patients_bp, url_prefix='/patients')
    app.register_blueprint(appointments_bp, url_prefix='/appointments')

    with app.app_context():
        from .utils.scheduler import schedule_updates

        # Initialize scheduler, In Progress
        schedule_updates(scheduler)
        scheduler.start()

        db.create_all()

    return app
