import pytest
import time

from simulation.cellular_automaton import CellularAutomaton
from logic.state_manager import StateManager
from logic.player import SimulationPlayer


def create_player():
	automaton = CellularAutomaton(5, 5, 0.5, 3, 5)
	manager = StateManager(automaton)
	manager.record_initial()
	player = SimulationPlayer(manager)
	return player

def test_step_forward_backward():
	player = create_player()
	player.step_forward()
	assert player.state_manager.current_step == 1
	player.step_backward()
	assert player.state_manager.current_step == 0

def test_simulation_run():
	player = create_player()
	player.set_speed(60)
	player.start()
	time.sleep(1.2)
	player.pause()
	assert player.state_manager.current_step > 0