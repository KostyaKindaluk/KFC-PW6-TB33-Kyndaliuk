import tkinter as tk
import ttkbootstrap as ttkb

MAX_CELLS = 1_000_000


class CreateSimulationWindow(ttkb.Toplevel):
	def __init__(self, master):
		super().__init__(master)
		self.transient(master)
		self.grab_set()
		self.title("Нова симуляція")
		self.geometry("320x550")

		ttkb.Label(self, text="Ширина поля:").pack(pady=5)
		self.width_var = tk.IntVar(value=50)
		ttkb.Entry(self, textvariable=self.width_var).pack(pady=5)

		ttkb.Label(self, text="Висота поля:").pack(pady=5)
		self.height_var = tk.IntVar(value=50)
		ttkb.Entry(self, textvariable=self.height_var).pack(pady=5)

		self.count_label = ttkb.Label(self, text="Клітин: 2500 ✔️", font=(None, 10, 'bold'))
		self.count_label.pack(pady=5)

		ttkb.Label(self, text="Інфікування (%):").pack(pady=5)
		inf_frame = ttkb.Frame(self)
		inf_frame.pack(fill=tk.X, pady=5)
		ttkb.Label(inf_frame, text="0").pack(side=tk.LEFT)
		self.p_inf_var = tk.DoubleVar(value=50.0)
		ttkb.Scale(inf_frame, from_=0, to=100, variable=self.p_inf_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
		ttkb.Label(inf_frame, text="100").pack(side=tk.LEFT)

		ttkb.Label(self, text="Час відновлення (кроки):").pack(pady=5)
		rec_frame = ttkb.Frame(self)
		rec_frame.pack(fill=tk.X, pady=5)
		ttkb.Label(rec_frame, text="0").pack(side=tk.LEFT)
		self.t_rec_var = tk.IntVar(value=10)
		ttkb.Scale(rec_frame, from_=0, to=100, variable=self.t_rec_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
		ttkb.Label(rec_frame, text="100").pack(side=tk.LEFT)

		ttkb.Label(self, text="Початково інфіковані:").pack(pady=5)
		self.init_inf_var = tk.IntVar(value=5)
		self.init_inf_entry = ttkb.Entry(self, textvariable=self.init_inf_var)
		self.init_inf_entry.pack(pady=5)
		self.init_inf_status = ttkb.Label(self, text="", font=(None, 10, 'bold'))
		self.init_inf_status.pack(pady=2)

		self.confirm_btn = ttkb.Button(self, text="Підтвердити", command=self.on_confirm)
		self.confirm_btn.pack(pady=20)

		for var in (self.width_var, self.height_var, self.init_inf_var):
			var.trace_add('write', self._validate_all)
		self._validate_all()

	def _validate_all(self, *args):
		try:
			w = self.width_var.get()
			h = self.height_var.get()
			total = w * h
		except (tk.TclError, ValueError):
			total = 0
		try:
			init = self.init_inf_var.get()
		except (tk.TclError, ValueError):
			init = 0

		if 1 <= total <= MAX_CELLS:
			count_emoji = '✔️'
			count_color = 'green'
			count_valid = True
		else:
			count_emoji = '❌'
			count_color = 'red'
			count_valid = False
		self.count_label.config(text=f"Клітин: {total} {count_emoji}", foreground=count_color)

		if count_valid and 1 <= init <= total:
			init_emoji = '✔️'
			init_color = 'green'
			init_valid = True
		else:
			init_emoji = '❌'
			init_color = 'red'
			init_valid = False
		self.init_inf_status.config(text=init_emoji, foreground=init_color)

		all_valid = count_valid and init_valid
		self.confirm_btn.config(state='normal' if all_valid else 'disabled')

	def on_confirm(self):
		w = self.width_var.get()
		h = self.height_var.get()
		p = self.p_inf_var.get() / 100.0
		t = self.t_rec_var.get()
		init = self.init_inf_var.get()
		self.master.setup_simulation(w, h, p, t, init)
		self.destroy()