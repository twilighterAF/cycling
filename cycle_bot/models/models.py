from pydantic import BaseModel


class Cycle(BaseModel):
    cycle: int
    start_time: int | float
    end_time: int | float
    started: bool
    paused: bool
    repeats: int


class UserCycle(BaseModel):
    users: int
    cycles: dict[int, Cycle]


class User(BaseModel):
    users: int
    cycles_started: bool
    cycles: dict[int, Cycle]