#....................................................................
# Session Manager:
#
# -Used by ./application.py
#
# This utility allows us to back-up our current program session_state
# before doing anything that could cause a crash.
#
# We can attempt to restore our previous session_state to recover 
# from a crash.
#....................................................................

import copy
from flask import session

# Stores current program state in a new instance.
# We use deepcopy to ensure no changes occur to
# our back-up in the event our current instance
# becomes corrupted.
def backup_session_data() -> None:
	session_state = session.get('state', {})
	history = session.get('state_history', [])
	history.append(copy.deepcopy(session_state))
	session['state_history'] = history

# Attempts to restore program state from the 
# most recent backup.
def restore_session_data() -> bool:
	history = session.get('state_history', [])
	if history:
		session['state'] = history.pop()
		session['state_history'] = history
		return True
	return False
