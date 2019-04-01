from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse

from . import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from input_field_test import Input_field_test

from django.core.mail import send_mail

error_message = None
error_message_success = "Ticket creation success"
error_message_empty_input = "Please fill in all input fields"
error_message_invalid_input = "Please ensure input fields are valid"
error_message_unauthorised = "Not authorised"  # used if the token sent by form does not tally with the one specified in /Source/website/input_field_test.py
error_message_forbidden_administrator = "This feature is not available to administrators"
error_message_forbidden_nonadministrator = "This feature is not available to non-administrators"
error_message_unknown_error = "Unknown error"  # thrown when we cant save ticket into model for some reason

@csrf_exempt
# csrf_exempt so that other websites may access this url without acquiring a csrf token
def remote_create(request):
	"""
	To be accessed by remote form (/TestForm/forms/views.py).. Checking of input validity will only be done here,
	not in the form.

	Prepared to receive the following key-values:
	title - title of ticket
	description - description of ticket
	name - Only alphabets
	phonenumber - Only integers
	email - Only alphabets, integers, one '@', and multiple '.'
	token - Any characters, used to validate that the one accessing our url is our forms (specificed in TestForm/forms/views.py and /Source/website/input_field_test.py)

	When input is valid, sends error_message as HttpResponse to form (even if input is valid). Possible error_messages include
	errro_message_success, errro_message_empty_input, errro_message_invalid_input, errro_message_unauthorised, error_message_unknown_error

	"""

	if (request.method == "POST"):
                name = None
                title = None
                email = None
                description = None
                phonenumber = None
                token = None


                try:
                        name = request.POST.get("name")
                        title = request.POST.get("title")
                        email = request.POST.get('email')
                        phonenumber = request.POST.get('phonenumber')
                        description = request.POST.get('description')
                        token = request.POST.get('token')
                except ValueError:
                        pass

                input_field_test = Input_field_test()
                username_validity = input_field_test.username(name)
                title_validity = input_field_test.ticket_title(title)
                email_validity = input_field_test.email(email)
                description_validity = input_field_test.ticket_description(description)
                phonenumber_validity = input_field_test.phonenumber(phonenumber)
                token_validity = input_field_test.token(token)

                if (len(username_validity)==1 and len(title_validity)==1 and len(email_validity)==1 and len(description_validity)==1 and len(phonenumber_validity)==1 and len(token_validity)==1):
                        try:
                                # input is valid
                                error_message = error_message_success
                                ticket = models.Ticket(ticket_id=id, title=title, resolved=0, read=0, description=description, user=name)
                                ticket.save()
                        except:
                                error_message = error_message_unknown_error
                else:
                        # input fields are not valid
                        empty_input_state = False
                        invalid_input_state = False
                        invalid_token_state = False

                        for i in username_validity:
                                if i == "empty":
                                        empty_input_state = True
                                elif i == "invalid value":
                                        invalid_input_state = True
                        for i in title_validity:
                                if i == "empty":
                                        empty_input_state = True
                                elif i == "invalid value":
                                        invalid_input_state = True
                        for i in email_validity:
                                if i == "empty":
                                        empty_input_state = True
                                elif i == "invalid value":
                                        invalid_input_state = True
                        for i in description_validity:
                                if i == "empty":
                                        empty_input_state = True
                                elif i == "invalid value":
                                        invalid_input_state = True
                        for i in phonenumber_validity:
                                if i == "empty":
                                        empty_input_state = True
                                elif i == "invalid value":
                                        invalid_input_state = True
                        for i in token_validity:
                                if i == "invalid value":
                                        invalid_token_state = True

                        if invalid_token_state:
                                # wrong token submitted
                                error_message = error_message_unauthorised
                        elif empty_input_state:
                                # input fields are empty
                                error_message = error_message_empty_input
                        elif invalid_input_state:
                                # input fields have invalid input
                                error_message = error_message_invalid_input

                return HttpResponse(error_message)


@csrf_exempt
def create(request):
        if (request.user.is_authenticated):
                # user is logged in
                if not (request.user.is_superuser):
                        # user is normal user
                        if request.method == 'POST':
                                username_validity = []
                                title_validity = []
                                email_validity = []
                                description_validity = []

                                input_field_test = Input_field_test()

                                try:
                                        id = 5
                                        username = request.POST.get("username")
                                        title = request.POST.get("title")
                                        email = request.POST.get('email')
                                        description = request.POST.get('description')
                                except ValueError:
                                        pass

                                username_validity = input_field_test.username(username)
                                title_validity = input_field_test.ticket_title(title)
                                email_validity = input_field_test.email(email)
                                description_validity = input_field_test.ticket_description(description)
                                # need to check whether notify by email/phonenumber?

                                ticket = models.Ticket(ticket_id=id, title=title, resolved=0, read=0, description=description, user=username)
                                ticket.save()
                                messages.add_message(request, messages.SUCCESS, 'Create Successful')

                                #send email notification to admin

                                send_mail('New Ticket Received', '{} has sent a new ticket'.format(username), "pleasedontlockthisemailthanks@gmail.com",
                                          ["admin@example.com"])
                                return render(request, 'ticketcreation/creation.html', {'error_message':error_message})
                        else:
                                return render(request, 'ticketcreation/creation.html', {'error_message':error_message})
                else:
                        # user is superuser
                        return HttpResponseForbidden(error_message_forbidden_administrator)
        else:
                return HttpResponseRedirect(reverse("login:index"))


def list(request):
	if (request.user.is_authenticated):
		# user is logged in
		if (request.user.is_superuser):
			# user is superuser
			list = models.Ticket.objects.all()
			return render(request, 'ticketcreation/show.html', {"list": list})
		else:
			# user is normal user
			return HttpResponseForbidden()
	else:
		return HttpResponseRedirect(reverse("login:index"))


def detail(request):
        if (request.user.is_authenticated):
                # user is loggged in
                if (request.user.is_superuser):
                        # user is superuser
                        id = request.GET.get("id")
                        try:
                                models.Ticket.objects.filter(id=id).update(read=1)
                                item = models.Ticket.objects.all().filter(id=id)
                        except:
                                raise HttpResponse(0)
                        return render(request, 'ticketcreation/detail.html', {"item": item[0], 'error_message':error_message})
                else:
                        # user is normal user
                        return HttpResponseRedirect(reverse("home:index"))
        else:
                # user is not logged in
                return HttpResponseRedirect(reverse("login:index"))



def delete(request):
        if (request.user.is_authenticated):
                # user is logged in
                if (request.user.is_superuser):
                        # user is superuser
                        column_id = request.GET.get("id")
                        print(column_id)
                        line = models.Ticket.objects.filter(id=column_id).delete()
                        list = models.Ticket.objects.all()
                        return render(request, 'ticketcreation/show.html', {"list": list, 'error_message':error_message})
                else:
                        # user is normal user
                        return HttpResponseRedirect(reverse("home:index"))
        else:
                # user is not logged in
                return HttpResponseRedirect(reverse("login:index"))



def resolve(request):
	if (request.user.is_authenticated):
		# user is logged in
		if (request.user.is_superuser):
			column_id = request.GET.get("id")
			try:
				models.Ticket.objects.filter(id=column_id).update(resolved=1)

			except:
				raise HttpResponse(0)
			list = models.Ticket.objects.all()
			return render(request, 'ticketcreation/show.html', {"list": list, "error_message":error_message})
		else:
			# user is normal user
			return HttpResponseRedirect(reverse("home:index"))
	else:
		return HttpResponseRedirect(reverse("login:index"))
