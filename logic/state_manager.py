import numpy as np

from simulation.cellular_automaton import CellularAutomaton


class StateManager:
    def __init__(self, automaton: CellularAutomaton):
        self.automaton = automaton
        self.history: list[np.ndarray] = []
        self.current_step: int = 0

    def record_initial(self):
        self.history = [self.automaton.get_state().copy()]
        self.current_step = 0

    def next(self):
        if self.current_step < len(self.history) - 1:
            self.current_step += 1
        else:
            self.automaton.step()
            self.history.append(self.automaton.get_state().copy())
            self.current_step += 1

    def prev(self):
        if self.current_step > 0:
            self.current_step -= 1

    def get_current(self) -> np.ndarray:
        return self.history[self.current_step]