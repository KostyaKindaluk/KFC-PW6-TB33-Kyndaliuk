import numpy as np
import random
from typing import Optional

from simulation.cell_state import CellState


class CellularAutomaton:
	def __init__(
		self,
		width: int,
		height: int,
		p_infect: float,
		t_recover: int,
		init_infected: int
	):
		self.width = width
		self.height = height
		self.p_infect = p_infect
		self.t_recover = t_recover

		self._state = np.full((height, width), CellState.HEALTHY, dtype=object)
		self._timer = np.zeros((height, width), dtype=int)

		total = width * height
		init_infected = min(init_infected, total)
		indices = random.sample(range(total), init_infected)
		for idx in indices:
			r, c = divmod(idx, width)
			self._state[r, c] = CellState.INFECTED
			self._timer[r, c] = 0


	def step(self) -> None:
		new_state = self._state.copy()
		new_timer = self._timer.copy()

		shifts = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
		for r in range(self.height):
			for c in range(self.width):
				st = self._state[r, c]
				if st == CellState.HEALTHY:
					infected_neighbors = 0
					for dr, dc in shifts:
						rr, cc = r + dr, c + dc
						if 0 <= rr < self.height and 0 <= cc < self.width:
							if self._state[rr, cc] == CellState.INFECTED:
								infected_neighbors += 1
					if infected_neighbors > 0 and random.random() < self.p_infect:
						new_state[r, c] = CellState.INFECTED
						new_timer[r, c] = 0
				elif st == CellState.INFECTED:
					if self._timer[r, c] + 1 >= self.t_recover:
						new_state[r, c] = CellState.RECOVERED
						new_timer[r, c] = 0
					else:
						new_timer[r, c] += 1
		self._state = new_state
		self._timer = new_timer
	
	def get_state(self) -> np.ndarray:
		return self._state.copy()