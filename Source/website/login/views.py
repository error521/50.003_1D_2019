from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import random
import string


from input_field_test import Input_field_test
from login.forms import LoginForm
from django.contrib import messages
from createuser.models import Extended_User as User
from email_functions import Email_functions

error_message_incorrect_userpass = "Login failure, username or password is incorrect"
error_message_empty_input = "Please fill in all input fields"
error_message_invalid_input = "Please ensure input fields are valid"
error_message_user_does_not_exist = "Invalid email, Please try again"
error_message_email_error = "Error in sending notifications to email"
error_message_success = "Password reset is successful. Please check your email for the new password."


@csrf_exempt
def index(request):
	#if request.user.is_authenticated:
	#    return HttpResponseRedirect('/home/')
	#else:

	error_message = None
	if request.method == 'POST':
		username = None
		password = None
		username_validity = []
		password_validity = []

		form = LoginForm(request.POST)

		try:
			username = request.POST['username']
			password = request.POST['password']
		except ValueError:
			pass

		# testing input field validity
		input_field_test = Input_field_test()
		username_validity = input_field_test.username(username)
		password_validity = input_field_test.password(password)

		if len(username_validity)==1 and len(password_validity)==1:
			user = authenticate(username=username, password=password)
			if user is not None:
				# login success
				login(request, user)  # saves user's ID in the session
				return HttpResponseRedirect(reverse("home:index"))
			else:
				# login failure
				error_message = error_message_incorrect_userpass
		else:
                        # input fields are not valid
                        empty_input_state = False
                        invalid_input_state = False

                        for i in username_validity:
                                if i == "empty":
                                        empty_input_state = True
                                elif i == "invalid value":
                                        invalid_input_state = True
                        for i in password_validity:
                                if i == "empty":
                                        empty_input_state = True
                                elif i == "invalid value":
                                        invalid_input_state = True

                        if empty_input_state:
                                # input fields are empty
                                error_message = error_message_empty_input
                        elif invalid_input_state:
                                # input fields have invalid input
                                error_message = error_message_invalid_input
                        else:
                                # uncaught error
                                return

	elif request.method == 'GET':
		pass

	messages.error(request, error_message)
	return render(request, 'login.html', {'form':LoginForm(), 'error_message':error_message})

def log_out(request):
	logout(request)
	return HttpResponseRedirect(reverse('login:index'))

@csrf_exempt
def reset_password(request):
	error_message = None
	if request.method == 'POST':
		email = None
		email_validity = None
		input_field_test = Input_field_test()

		try:
			email = request.POST["email"]
		except ValueError:
			pass

		email_validity = input_field_test.email_reset_password(email)
		print(email_validity)

		if len(email_validity) == 1:
			# input field is valid
			user = User.objects.get(email=email)
			if user == None:
				error_message = error_message_user_does_not_exist

			else:
				new_password = "SHAME_ON_ME_"
				new_password += ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
				email_functions = Email_functions()
				user.set_password(new_password)
				user.save()
				print("new_password: {0}".format(new_password))

				if email_functions.login_forget_password(user.username, user.email, new_password) == email_functions.email_sending_success:
					error_message = error_message_success
				else:
					error_message = error_message_email_error

		else:
			# input fields are not valid
			empty_input_state = False
			invalid_input_state = False

			for i in email_validity:
				if i == "empty":
					empty_input_state = True
				elif i == "invalid value":
					invalid_input_state = True

			if empty_input_state:
				# input fields are empty
				error_message = error_message_empty_input
			elif invalid_input_state:
				# input fields have invalid input
				error_message = error_message_invalid_input


		messages.error(request, error_message)
		return render(request, 'forgot-password.html', {'error_message': error_message} )
	else:
		return render(request, 'forgot-password.html' )

