import pytest

from simulation.cellular_automaton import CellularAutomaton
from logic.state_manager import StateManager


def create_manager():
	automaton = CellularAutomaton(5, 5, 0.0, 5, 5)
	manager = StateManager(automaton)
	manager.record_initial()
	return manager

def test_initial_record():
	manager = create_manager()
	assert len(manager.history) == 1
	assert manager.current_step == 0

def test_forward_backward():
	manager = create_manager()
	manager.next()
	assert manager.current_step == 1
	manager.prev()
	assert manager.current_step == 0

def test_history_growth():
	manager = create_manager()
	for _ in range(3):
		manager.next()
	assert len(manager.history) == 4