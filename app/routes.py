from app.api.auth import SignupAPI

def initialize_routes(api):
    api.add_resource(SignupAPI, '/api/auth/signup')