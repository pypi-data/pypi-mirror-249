from slinn import Server, Filter


class Dispatcher:
	def __init__(self, hosts: list=None):
		self.handles = []
		self.hosts = hosts if hosts is not None else ['.*']
		
	def route(self, filter: Filter):
		def decorator(func):
			self.handles.append(Server.Handle(filter, func))
		return decorator	