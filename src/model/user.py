import json

class User(object):	
	def __init__(self, username, password):
		self.username = username
		self.password = password

	def to_json(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)