from abc import ABC, abstractmethod


class Observer(ABC):
	@abstractmethod
	def update(self):
		pass

class Subject:
	def __init__(self):
		self._observers: list[Observer] = []


	def subscribe(self, obs: Observer):
		self._observers.append(obs)

	def unsubscribe(self, obs: Observer):
		self._observers.remove(obs)

	def notify(self):
		for obs in self._observers:
			obs.update()