from dataclasses import field
from pydantic import BaseModel


class Mask(BaseModel):
    name: str
    pattern: str


class Anonymisation(BaseModel):
    masks: list[Mask] = field(default_factory=list)


class AppConfig(BaseModel):
    anonymisation: Anonymisation
