from resources.token import TokenResource
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from Config import Config
from extensions import db, jwt
from resources.user import MeResource, UserListResource, UserResource

from resources.instruction import InstructionPublic, InstructionListResource, InstructionResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.app_context().push()
    register_extensions(app)
    register_resources(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app,db)
    jwt.init_app(app)


def register_resources(app):
    api = Api(app)

    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(TokenResource, '/token')
    api.add_resource(InstructionListResource, '/instructions')
    api.add_resource(InstructionResource, '/instructions/<int:instruction_id>')
    api.add_resource(InstructionPublic, '/instructions/<int:instruction_id>/publish')
    api.add_resource(MeResource, '/me')


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000, debug=True)
