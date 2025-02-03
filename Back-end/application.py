from flask import Flask

application = Flask(__name__)

@application.route('/')
def index():
	return "Hello, AWS Elastic Beanstalk! lol"

if __name__ == "__main__":
    application.run()