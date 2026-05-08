from typing import Optional
from datetime import datetime
import uuid

class User:
    def __init__(self, id: str, email: str, hashed_password: str, created_at: Optional[datetime] = None):
        self.id = id
        self.email = email
        self.hashed_password = hashed_password
        self.created_at = created_at or datetime.utcnow()

class Train:
    def __init__(self, id: str, weight: int, train_cars: int):
        self.id = id
        self.weight = weight
        self.train_cars = train_cars

class Line:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

class Track:
    def __init__(self, id: str, id_line: str, length: int, bending: int, elevation: int):
        self.id = id
        self.id_line = id_line
        self.length = length
        self.bending = bending
        self.elevation = elevation