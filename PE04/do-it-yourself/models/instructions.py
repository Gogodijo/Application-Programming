from extensions import db


instruction_list = []


def get_last_id():
    if instruction_list:
        last_instruction = instruction_list[-1]
    else:
        return 1
    return last_instruction.id + 1


class Instruction(db.Model):
    __tablename__ = 'instruction'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    steps = db.Column(db.String(300))
    tools = db.Column(db.String(300))
    cost = db.Column(db.Integer())
    duration = db.Column(db.Integer())
    is_publish = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def data(self):
        return{
            'id' : self.id,
            'name' : self.name,
            'description' : self.description,
            'steps' : self.steps,
            'tools' : self.tools,
            'cost' : self.cost,
            'duration' : self.duration,
            'user_id' : self.user_id
        }

    @classmethod
    def get_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all_instructions(cls):
        return cls.query.filter_by(is_publish = True).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

