from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.instructions import Instruction, instruction_list


class InstructionListResource(Resource):

    def get(self):

        data = [ instruction.data() for instruction in Instruction.get_all_instructions()]

        return {'data': str(data)}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        instruction = Instruction(
            name=data["name"],
            description=data["description"],
            steps=data["steps"],
            tools=data["tools"],
            cost=data["cost"],
            duration=data["duration"]
        )
        instruction.save()

        return  HTTPStatus.CREATED


class InstructionResource(Resource):

    def get(self, instruction_id):
        instruction = Instruction.get_by_id(instruction_id)

        if instruction is None:
            return {'Message': 'Instruction not found'}, HTTPStatus.NOT_FOUND

        return instruction.data, HTTPStatus.OK


class InstructionPublic(Resource):

    def put(self, instruction_id):
        instruction = next((instruction for instruction in instruction_list if instruction.id ==
                            instruction_id), None)

        if instruction is None:
            return {'Message': 'Instruction not found'}, HTTPStatus.NOT_FOUND

        instruction.is_publish = True

        return {}, HTTPStatus.NO_CONTENT

    def delete(self, instruction_id):
        instruction = next((instruction for instruction in instruction_list if instruction.id ==
                            instruction_id), None)

        if instruction is None:
            return {'Message': 'Instruction not found'}, HTTPStatus.NOT_FOUND

        instruction.is_publish = False

        return {}, HTTPStatus.NO_CONTENT
