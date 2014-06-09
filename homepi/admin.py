import os
from flask import Flask, url_for, redirect, render_template, request

from wtforms import form, fields, validators
from flask.ext import admin, login
from flask.ext.login import UserMixin
from flask.ext.admin import helpers, expose
from IPython import embed
from homepi import app

class User(UserMixin):
	def __init__(self, name, password, id, active=True):
		self.id = id
		self.name = name
		self.active = active
		self.password = password

	def get_id(self):
		return self.id

	def is_active(self):
		return self.active

	def get_auth_token(self):
		return make_secure_token(self.name, key=app.config['AUTH_TOKEN_KEY'])

# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
	login = fields.TextField(validators=[validators.required()])
	password = fields.PasswordField(validators=[validators.required()])

	def validate_login(self, field):
		user = self.get_user()

		if user is None:
			raise validators.ValidationError('Invalid user')
		if user.password != self.password.data:
			raise validators.ValidationError('Invalid password')

	def get_user(self):
		return USERS[self.login.data]

# Initialize flask-login
def init_login():
	login_manager = login.LoginManager()
	login_manager.init_app(app)

	# Create user loader function
	@login_manager.user_loader
	def load_user(user_id):
		return USERS_ID[user_id]

# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):
	@expose('/')
	def index(self):
		if not login.current_user.is_authenticated():
			return redirect(url_for('.login_view'))
		return super(MyAdminIndexView, self).index()
	@expose('/login/', methods=('GET', 'POST'))
	def login_view(self):
		# handle user login
		form = LoginForm(request.form)
		if helpers.validate_form_on_submit(form):
			user = form.get_user()
			login.login_user(user)

		if login.current_user.is_authenticated():
			return redirect(url_for('index'))
		self._template_args['form'] = form
		return super(MyAdminIndexView, self).index()

	@expose('/logout/')
	def logout_view(self):
		login.logout_user()
		return redirect(url_for('.index'))
# Initialize flask-login
init_login()
admin = admin.Admin(app, 'Auth', index_view=MyAdminIndexView(), base_template='master.html')
USERS = {}
USERS[app.config['USERNAME']] = User(app.config['USERNAME'],app.config['PASSWORD'],1)
USERS_ID = {}
for name,user in USERS.items():
	USERS_ID[user.id] = user

