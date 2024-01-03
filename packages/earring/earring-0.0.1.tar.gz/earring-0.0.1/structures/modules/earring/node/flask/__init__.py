
from flask import Flask

def build ():
	app = Flask(__name__)

	@app.route("/")
	def hello_world():
		return "<p>Hello, World!</p>"
		
	return app;