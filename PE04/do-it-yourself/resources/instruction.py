import http
from flask import request
from flask_migrate import current
from flask_restful import Resource
from http import HTTPStatus
from models.instructions import Instruction
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional

class InstructionListResource(Resource):

    def get(self):

        data = [ instruction.data() for instruction in Instruction.get_all_published()]

        return {'data': str(data)}, HTTPStatus.OK

    @jwt_required
    def post(self):
        data = request.get_json()
        current_user = get_jwt_identity()
        instruction = Instruction(
            name=data["name"],
            description=data["description"],
            steps=data["steps"],
            tools=data["tools"],
            cost=data["cost"],
            duration=data["duration"],
            user_id = current_user
        )
        instruction.save()

        return  HTTPStatus.CREATED


class InstructionResource(Resource):

    @jwt_optional
    def get(self, instruction_id):
        instruction = Instruction.get_by_id(instruction_id)

        if instruction is None:
            return {'Message': 'Instruction not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if instruction.is_publish == False and instruction.user_id != current_user:
            return {'message': 'Access is not allower'}, HTTPStatus.FORBIDDEN

        return instruction.data(), HTTPStatus.OK



class InstructionPublic(Resource):

    @jwt_required
    def put(self, instruction_id):
        
        data = request.get_json()

        instruction = Instruction.get_by_id(instruction_id=instruction_id)

        if instruction is None:
            return {'message': 'Instruction not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != instruction.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        instruction.name = data["name"]
        instruction.description = data["description"]
        instruction.steps = data["steps"]
        instruction.tools = data["tools"]
        instruction.cost = data["cost"]
        

        return {}, HTTPStatus.NO_CONTENT

    def delete(self, instruction_id):
        instruction = next((instruction for instruction in instruction_list if instruction.id ==
                            instruction_id), None)

        if instruction is None:
            return {'Message': 'Instruction not found'}, HTTPStatus.NOT_FOUND

        instruction.is_publish = False

        return {}, HTTPStatus.NO_CONTENT
