#..................................................................
# Main Application
#
# Routes requests and manages program state.
#..................................................................

from flask import Flask, session, request, redirect, url_for, flash
from Utils.state_manager import backup_state, restore_state

application = Flask(__name__)
application.secret_key = 'your_secret_key'

@application.route('/')
def index():
	return "Capsoft website coming soon!"

@application.route('/modify', methods=['POST'])
def modify():
	backup_state()  # Backup current state before modifying
	state = session.get('state', {})
	state['data'] = request.form.get('data')
	session['state'] = state
	return redirect(url_for('index'))

@application.route('/abort')
def abort():
	if restore_state():
		flash("Changes aborted and state restored.")
	else:
		flash("No previous state found.")
	return redirect(url_for('index'))

if __name__ == "__main__":
	application.run()
