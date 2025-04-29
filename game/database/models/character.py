from sqlalchemy import Column, Integer, String
from game.database.base import Base

class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)

    def __init__(self, name: str):
        self.name = name

    def get_name(self):
        return self.name

    def __repr__(self):
        return f"<Character(name={self.name}, level={self.level}, experience={self.experience})>"