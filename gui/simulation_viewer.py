import tkinter as tk
import numpy as np

from simulation.cell_state import CellState


class SimulationViewer(tk.Canvas):
	def __init__(self, master, width=600, height=600, **kwargs):
		super().__init__(master, width=width, height=height, bg='white', **kwargs)
		self.width = width
		self.height = height

		self.scale = 5.0 
		self.offset_x = 0
		self.offset_y = 0

		self._drag_data = {'x': 0, 'y': 0}
		self._state = None

		self.bind('<ButtonPress-1>', self._on_button_press)
		self.bind('<B1-Motion>', self._on_move_press)
		self.bind('<MouseWheel>', self._on_mousewheel)
		self.bind('<Button-4>', self._on_mousewheel)
		self.bind('<Button-5>', self._on_mousewheel)


	def _on_button_press(self, event):
		self._drag_data['x'] = event.x
		self._drag_data['y'] = event.y

	def _on_move_press(self, event):
		dx = event.x - self._drag_data['x']
		dy = event.y - self._drag_data['y']
		self._drag_data['x'] = event.x
		self._drag_data['y'] = event.y
		self.offset_x += dx
		self.offset_y += dy
		self.redraw()

	def _on_mousewheel(self, event):
		if event.num == 4 or event.delta > 0:
			factor = 1.1
		elif event.num == 5 or event.delta < 0:
			factor = 0.9
		else:
			factor = 1.0

		old_scale = self.scale
		self.scale *= factor
		self.scale = max(1.0, min(self.scale, 50.0))

		x = self.canvasx(event.x)
		y = self.canvasy(event.y)
		self.offset_x = event.x - (x * self.scale / old_scale - self.offset_x)
		self.offset_y = event.y - (y * self.scale / old_scale - self.offset_y)
		self.redraw()

	def draw_state(self, state: np.ndarray):
		self._state = state
		self.redraw()

	def redraw(self):
		self.delete('all')
		if self._state is None:
			return
		h, w = self._state.shape
		cell_size = self.scale
		for r in range(h):
			for c in range(w):
				x1 = c * cell_size + self.offset_x
				y1 = r * cell_size + self.offset_y
				x2 = x1 + cell_size
				y2 = y1 + cell_size
				if x2 < 0 or y2 < 0 or x1 > self.width or y1 > self.height:
					continue
				cell = self._state[r, c]
				if cell == CellState.HEALTHY:
					color = '#f0f0f0'
				elif cell == CellState.INFECTED:
					color = '#e74c3c'
				else:
					color = '#2ecc71'
				self.create_rectangle(x1, y1, x2, y2, fill=color, outline='')