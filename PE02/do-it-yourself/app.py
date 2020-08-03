from flask import Flask
from flask_restful import Api

from resources.instruction import InstructionPublic, InstructionListResource, InstructionResource

app = Flask(__name__)
api = Api(app)

api.add_resource(InstructionListResource, '/instructions')
api.add_resource(InstructionResource, '/instructions/<int:instruction_id>')
api.add_resource(InstructionPublic, '/instructions/<int:instruction_id>/publish')

if __name__ == '__main__':
    app.run(port=5000, debug=True)