from flask import Flask

application = Flask(__name__)

@application.route('/')
def index():
	return "Capsoft website coming soon!"

if __name__ == "__main__":
    application.run()