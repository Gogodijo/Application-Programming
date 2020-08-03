from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.instructions import Instruction, instruction_list


class InstructionListResource(Resource):

    def get(self):

        data = []

        for instruction in instruction_list:
            if instruction.is_publish:
                data.append(instruction.data)

        return {'data': data}, HTTPStatus.OK


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

        instruction_list.append(instruction)

        return instruction.data, HTTPStatus.CREATED


class InstructionResource(Resource):

    def get(self, instruction_id):
        instruction = next((instruction for instruction in instruction_list if instruction.id ==
                            instruction_id and instruction.is_publish == True), None)

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

