import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb

from logic.player import SimulationPlayer
from logic.state_manager import StateManager
from simulation.cell_state import CellState
from simulation.cellular_automaton import CellularAutomaton
from gui.create_simulation_window import CreateSimulationWindow
from gui.simulation_viewer import SimulationViewer


BUTTON_STYLES = {
	'create': {'bootstyle': 'success-outline'},
	'delete': {'bootstyle': 'danger-outline'},
	'start': {'bootstyle': 'success'},
	'pause': {'bootstyle': 'warning'},
	'prev': {'bootstyle': 'info'},
	'next': {'bootstyle': 'info'}
}

class MainWindow(ttkb.Window):
	def __init__(self):
		super().__init__(themename='flatly')
		self.title("Симуляція епідемії")
		self.geometry("800x600")

		self.canvas = SimulationViewer(self, width=600, height=600)
		self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		ctrl = ttkb.Frame(self, padding=10)
		ctrl.pack(side=tk.RIGHT, fill=tk.Y)

		self.btn_create = ttkb.Button(ctrl, text="Створити симуляцію",
			command=self.open_create_window,
			**BUTTON_STYLES['create'])
		self.btn_delete = ttkb.Button(ctrl, text="Видалити симуляцію",
			command=self.delete_simulation,
			state="disabled",
			**BUTTON_STYLES['delete'])
		self.btn_start = ttkb.Button(ctrl, text="Старт",
			command=self.start_sim,
			state="disabled",
			**BUTTON_STYLES['start'])
		self.btn_pause = ttkb.Button(ctrl, text="Пауза",
			command=self.pause_sim,
			state="disabled",
			**BUTTON_STYLES['pause'])
		self.btn_prev = ttkb.Button(ctrl, text="Крок назад",
			command=self.step_back,
			state="disabled",
			**BUTTON_STYLES['prev'])
		self.btn_next = ttkb.Button(ctrl, text="Крок вперед",
			command=self.step_forward,
			state="disabled",
			**BUTTON_STYLES['next'])
		for btn in (self.btn_create, self.btn_delete,
			self.btn_start, self.btn_pause,
			self.btn_prev, self.btn_next):
			btn.pack(fill=tk.X, pady=3)

		ttkb.Label(ctrl, text="Швидкість (кроків/хв)").pack(pady=(20, 0))
		slider_frame = ttkb.Frame(ctrl)
		slider_frame.pack(fill=tk.X, pady=5)
		ttkb.Label(slider_frame, text="1").pack(side=tk.LEFT, padx=(0,5))
		self.speed_slider = ttkb.Scale(slider_frame, from_=1, to=600,
			command=self.on_speed_change)
		self.speed_slider.set(60)
		self.speed_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
		ttkb.Label(slider_frame, text="600").pack(side=tk.LEFT, padx=(5,0))

		ttkb.Label(ctrl, text="Крок:").pack(pady=(20, 0))
		self.step_label = ttkb.Label(ctrl, text="0", font=('TkDefaultFont', 12, 'bold'))
		self.step_label.pack()

		ttkb.Separator(ctrl).pack(fill=tk.X, pady=10)
		ttkb.Label(ctrl, text="Стан клітин:").pack()
		self.healthy_label = ttkb.Label(ctrl, text="Здорові: 0")
		self.infected_label = ttkb.Label(ctrl, text="Інфіковані: 0")
		self.recovered_label = ttkb.Label(ctrl, text="Відновлені: 0")
		for lbl in (self.healthy_label, self.infected_label, self.recovered_label):
			lbl.pack(anchor='w', padx=5)

		self.player: SimulationPlayer | None = None


	def open_create_window(self):
		CreateSimulationWindow(self)

	def setup_simulation(self, width, height, p_inf, t_rec, init_inf):
		automaton = CellularAutomaton(width, height, p_inf, t_rec, init_inf)
		sm = StateManager(automaton)
		self.player = SimulationPlayer(sm)
		self.player.subscribe(self)

		self.btn_create.config(state='disabled')
		self.btn_delete.config(state='normal')
		self.btn_start.config(state='normal')
		self.btn_pause.config(state='disabled')
		self.btn_prev.config(state='normal')
		self.btn_next.config(state='normal')
		self.redraw()

	def delete_simulation(self):
		if self.player: self.player.pause()
		self.player = None
		self.canvas.delete('all')

		self.btn_create.config(state='normal')
		self.btn_delete.config(state='disabled')
		self.btn_start.config(state='disabled')
		self.btn_pause.config(state='disabled')
		self.btn_prev.config(state='disabled')
		self.btn_next.config(state='disabled')

		self.step_label.config(text="0")
		self.healthy_label.config(text="Здорові: 0")
		self.infected_label.config(text="Інфіковані: 0")
		self.recovered_label.config(text="Відновлені: 0")

	def start_sim(self):
		if self.player and not self.player._running:
			self.player.start()
			self.btn_start.config(state='disabled')
			self.btn_pause.config(state='normal')

	def pause_sim(self):
		if self.player and self.player._running:
			self.player.pause()
			self.btn_start.config(state='normal')
			self.btn_pause.config(state='disabled')

	def step_forward(self):
		if self.player:
			self.player.step_forward()
			self.btn_start.config(state='normal')
			self.btn_pause.config(state='disabled')

	def step_back(self):
		if self.player:
			self.player.step_backward()
			self.btn_start.config(state='normal')
			self.btn_pause.config(state='disabled')

	def on_speed_change(self, val):
		if self.player:
			self.player.set_speed(float(val))

	def update(self):
		self.after(0, self.redraw)

	def redraw(self):
		if not self.player:
			return
		state = self.player.state_manager.get_current()
		self.canvas.draw_state(state)
		step = self.player.state_manager.current_step + 1
		self.step_label.config(text=str(step))

		flat = state.flatten()
		self.healthy_label.config(text=f"Здорові: {int((flat==CellState.HEALTHY).sum())}")
		self.infected_label.config(text=f"Інфіковані: {int((flat==CellState.INFECTED).sum())}")
		self.recovered_label.config(text=f"Відновлені: {int((flat==CellState.RECOVERED).sum())}")