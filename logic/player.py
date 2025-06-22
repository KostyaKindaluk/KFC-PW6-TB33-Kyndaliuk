import threading
import time

from logic.observer import Subject
from logic.state_manager import StateManager


class SimulationPlayer(Subject):
	def __init__(self, state_manager: StateManager):
		super().__init__()
		self.state_manager = state_manager
		self.state_manager.record_initial()
		self.speed: float = 1.0
		self._running = False
		self._thread: threading.Thread | None = None


	def start(self):
		if not self._running:
			self._running = True
			self._thread = threading.Thread(target=self._run_loop, daemon=True)
			self._thread.start()

	def _run_loop(self):
		while self._running:
			time.sleep(1 / self.speed)
			self.state_manager.next()
			self.notify()

	def pause(self):
		self._running = False

	def step_forward(self):
		self.state_manager.next()
		self.notify()

	def step_backward(self):
		self.state_manager.prev()
		self.notify()

	def set_speed(self, steps_per_minute: float):
		self.speed = steps_per_minute / 60