# model/state.py
from dataclasses import dataclass

@dataclass
class ScenarioState:
    welcomed: bool = False
    running: bool = False