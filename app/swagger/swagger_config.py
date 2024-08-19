from flask_restx import Api

def initialize_swagger(app):

    # Adding Authorization to Swagger
    authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Add a Bearer token to authorize'
        }
    }

    api = Api(
        app,
        version='1.0',
        title='Hospital API',
        description='API for managing hospital resources for test assessment',
        doc='/swagger/',
        authorizations=authorizations,
        security='Bearer'
    )

    # Register namespaces
    from ..routes.auth import ns as auth_ns
    from ..routes.employees import ns as employees_ns
    from ..routes.doctors import ns as doctors_ns
    from ..routes.patients import ns as patients_ns
    from ..routes.appointments import ns as appointments_ns

    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(employees_ns, path='/employees')
    api.add_namespace(doctors_ns, path='/doctors')
    api.add_namespace(patients_ns, path='/patients')
    api.add_namespace(appointments_ns, path='/appointments')
