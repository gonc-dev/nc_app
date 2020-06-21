from app.models import Customer
from django.contrib.auth.backends import ModelBackend

class EmailAuthBackend(ModelBackend):
	"""
	Email Authentication Backend

	Allows a user to sign in using an email/password pair rather than
	a username/password pair.
	"""
 
	def authenticate(self, request, username=None, password=None):
		""" Authenticate a user based on email address as the user name. """
		try:
			user = Customer.objects.get(email=username)
			if user.check_password(password):
				return user
		except Customer.DoesNotExist:
			return None

	def get_user(self, user_id):
		""" Get a User object from the user_id. """
		try:
			return Customer.objects.get(pk=user_id)
		except Customer.DoesNotExist:
			return None