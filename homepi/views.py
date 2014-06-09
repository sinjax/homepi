from homepi import app
from flask.ext.login import login_required
from flask.ext import login 
from flask import render_template,redirect,url_for


@app.route("/", methods=["GET"])
def index(): 
	if not login.current_user.is_authenticated():
		return redirect(url_for('admin.login_view'))
	return "Logged in!"
	