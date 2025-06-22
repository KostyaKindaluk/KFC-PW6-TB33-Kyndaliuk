import pytest
import numpy as np

from simulation.cellular_automaton import CellularAutomaton
from simulation.cell_state import CellState


def test_initial_infected_count():
	automaton = CellularAutomaton(10, 10, 0.0, 5, 10)
	state = automaton.get_state()
	infected_count = np.sum(state == CellState.INFECTED)
	assert infected_count == 10

def test_infection_progress():
	automaton = CellularAutomaton(5, 5, 1.0, 1, 1)
	for _ in range(3):
			automaton.step()
	state = automaton.get_state()
	assert np.any(state == CellState.RECOVERED)

def test_no_infection_without_contacts():
	automaton = CellularAutomaton(3, 3, 0.0, 3, 0)
	automaton.step()
	state = automaton.get_state()
	assert np.all(state == CellState.HEALTHY)