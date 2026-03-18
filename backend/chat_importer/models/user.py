from chat_importer.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True, index=True)

    messages = db.relationship("Message", back_populates="sender", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
