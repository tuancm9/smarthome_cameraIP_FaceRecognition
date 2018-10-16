class A:
	name="ll"
	def __init__(self,name):
		self.name=name
	def run(self):
		print self.name
	def start(self):
		self.run() 
B = A("tuan")
B.start()
