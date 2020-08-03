instruction_list = []


def get_last_id():
    if instruction_list:
        last_instruction = instruction_list[-1]
    else:
        return 1
    return last_instruction.id + 1


class Instruction:

    def __init__(self, name, description, steps, tools, cost, duration):
        self.id = get_last_id()
        self.name = name
        self.description = description
        self.steps = steps
        self.tools = tools
        self.cost = cost
        self.duration = duration
        self.is_publish = False

    @property
    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'steps': self.steps,
            'tools': self.tools,
            'cost': self.cost,
            'duration': self.duration
        }
