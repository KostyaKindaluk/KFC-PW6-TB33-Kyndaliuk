import pytest
import threading
import time

from gui.main_window import MainWindow
import tkinter as tk


@pytest.fixture
def app():
	root = MainWindow()
	yield root
	root.destroy()

def test_main_window_launch(app):
	assert isinstance(app, MainWindow)
	assert app.winfo_exists()

def test_simulation_create(app):
	app.setup_simulation(10, 10, 0.5, 5, 2)
	assert app.player is not None
	assert app.player.state_manager.get_current().shape == (10, 10)

def test_full_gui_cycle(app):
	app.setup_simulation(5, 5, 0.3, 4, 3)
	app.start_sim()
	time.sleep(0.1)
	app.pause_sim()
	app.step_forward()
	app.step_back()
	app.delete_simulation()