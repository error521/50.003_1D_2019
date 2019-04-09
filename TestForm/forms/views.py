from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import BasicForm
from input_field_test import Input_field_test

import requests


error_message_success = "Form submitted!"
error_message_empty_input = "Please fill in all input fields"
error_message_invalid_input = "Please ensure input fields are valid"

# messages sent by Source website after submitting forms
received_message_success = "Ticket creation success"
received_message_empty_input = "Please fill in all input fields"
received_message_invalid_input = "Please ensure input fields are valid"
received_message_unauthorised = "Not authorised"
received_message_unknown_error = "Unknown error"


token = "UKJHhgvIU&^%$bvd#$HJ"
target_url = "http://127.0.0.1:3000/ticket_creation/"
data = {"title":None, "description":None, "name":None, "phonenumber":None, "email":None, "token":None}


def basic_form(request):
	error_message = None
	if request.method == 'POST':
		form = BasicForm()

		title = request.POST.get('title')
		description = request.POST.get('description')
		name = request.POST.get('name')
		phonenumber = request.POST.get('phonenumber')
		email = request.POST.get('email')
		r = requests.post(target_url, data={"title":title, "description":description, "name":name, "phonenumber":phonenumber, "email":email, "token":token, "is_remote":"True"})

		error_message = r.text

		return render(request, 'forms/index.html', {'form': form, 'error_message':error_message})
	else:
		form = BasicForm()
		return render(request, 'forms/index.html', {'form': form, 'error_message':error_message})
