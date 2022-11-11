from Flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Person:
	db_name = 'test'
	def __init__(self, data):
		self.id = data['id']
		self.first_name = data['first_name']
		self.last_name = data['last_name']
		self.email = data['email']
		self.password = data['password']
		self.created_at = data['created_at']
		self.updated_at = data['updated_at']
		self.user_id = None

	@classmethod
	def save(cls, data):
		query = "INSERT INTO Users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
		return connectToMySQL(cls.db_name).query_db(query, data)

	@classmethod
	def get__by_email(cls, data):
		query = "SELECT * FROM Users WHERE email = %(email)s;"
		results = connectToMySQL(cls.db_name).query_db(query, data)
		return cls(results[0])

	@classmethod
	def get_all(cls, data):
		query = "SELECT * FROM Users "
		results = connectToMySQL(cls.db_name).query_db(query)
		users = []
		for row in results:
			users.append(cls(row))
		return users

	@classmethod
	def get_by_id(cls, user_id):
		data = {
			'id': user_id #this is using the key to set the user_id
		}
		query = "SELECT * FROM users WHERE id = %(id)s"
		results = connectToMySQL(cls.db_name).query_db(query, data)
		return cls(results[0])

	@staticmethod
	def validate(user):
		is_valid = True
		query = "SELECT * FROM Users WHERE email = %(email)s;"
		results = connectToMySQL(Person.db_name).query_db(query, user)
		if len(results) >= 1:
			flash("Email Taken", "Register")
			is_valid = False
		if not  EMAIL_REGEX.match(user['email']):
			flash("Invaild Email", "Register")
			is_valid = False
		if len(user['first_name']) < 2:
			flash("First Name not long enough", "Register")
			is_valid = False
		if len(user['last_name']) < 2:
			flash("Last Name not long enough", "Register")
			is_valid = False
		if len(user['password']) < 8:
			flash("Password is def not long enough", "Register")
			is_valid = False
		if user['password'] != user['confirm']:
			flash("PASSWORDS DO NOT MATCH", "Register")
			is_valid = False
		return is_valid