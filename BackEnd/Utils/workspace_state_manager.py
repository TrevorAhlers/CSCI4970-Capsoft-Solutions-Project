#....................................................................
# Workspace State Manager:
#
# Uses WorkspaceState model to save workspace state to DB
#....................................................................

from flask import session

#TODO: load workspace state -> DB JSON object populates model -> model is outputted to frontend

#TODO: change to workspace attribute -> set as current workspace state in DB under name "current" *might be resource intensive

#TODO: restore default -> create new model with default values and update db under name "current" & "default" -> model is outputted to frontend

#TODO: save custom workspace(name) -> save workspace data in DB under name

#TODO: delete custom workspace in DB by name