from flask import Flask, jsonify, request
from http import HTTPStatus

instructions = [{
    "id": 1,
    "name": "Paint a wall",
    "description": "Instructions how to paint a wall",
    "steps": [" Clean the wall", "Tape the trim",
              "Roll the primer onto the wall",
              "Paint the trim", "Remove the painter's tape"],
    "tools": ["painter's tape", "primer", "paint", "paint roller",
              "paint tray", " paintbrush"],
    "cost": 100,
    "duration": 8
},
    {
        "id": 2,
        "name": "Build a table",
        "steps": ["Take out parts", "Read instructions", "Get frustrated", "Call Ikea customer support", "Get Drunk",
                  "Try again tomorrow"],
        "tools": ["Hammer", "Screwdriver", "Beer"],
        "cost": 200,
        "duration": 16

    }]

app = Flask(__name__)


@app.route("/instructions", methods=["GET"])
def get_instructions():
    return jsonify({"data": instructions})


@app.route("/instructions/<int:instruction_id>", methods=["GET"])
def get_instruction(instruction_id):
    instruction = next((instruction for instruction in instructions if int(instruction["id"]) == instruction_id), None)
    if instruction:
        return jsonify(instruction)

    return jsonify({"message": "Instruction not found"}), HTTPStatus.NOT_FOUND


@app.route("/instructions", methods=["POST"])
def create_instruction():
    data = request.get_json()
    instruction = {
        "id": len(instructions) + 1,
        "name": data.get("name"),
        "steps": data.get("steps"),
        "tools": data.get("tools"),
        "cost": data.get("cost"),
        "duration": data.get("duration")
    }
    instructions.append(instruction)
    return jsonify(instruction), HTTPStatus.CREATED


@app.route("/instructions/<int:instruction_id>", methods=["PUT"])
def update_instruction(instruction_id):
    instruction = next((instruction for instruction in instructions if int(instruction["id"]) == instruction_id), None)
    if not instruction:
        return jsonify({"Message:": "Instruction not found"}), HTTPStatus.NOT_FOUND

    data = request.get_json()

    instruction.update({
        "name": data.get("name"),
        "steps": data.get("steps"),
        "tools": data.get("tools"),
        "cost": data.get("cost"),
        "duration": data.get("duration")
    })

    return jsonify(instruction)


@app.route("/instructions/<int:instruction_id>", methods=["DELETE"])
def delete_instruction(instruction_id):
    instruction = next((instruction for instruction in instructions if int(instruction["id"]) == instruction_id), None)
    if not instruction:
        return jsonify({"Message:": "Instruction not found"}), HTTPStatus.NOT_FOUND

    instructions.remove(instruction)
    return jsonify({"Message: ": "Deleted instruction successfully"}), HTTPStatus.NO_CONTENT


if __name__ == "__main__":
    app.run()
