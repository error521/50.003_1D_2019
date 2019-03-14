from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


@csrf_exempt
def create(request):
	if (request.user.is_authenticated):
		# user is logged in
		if not (request.user.is_superuser):
			# user is normal user
			if request.method == 'POST':
				id = 5
				username = request.POST.get("username")
				title = request.POST.get("title")
				print(username)
				email = request.POST.get('email')
				description = request.POST.get('description')
				print(username)
				ticket = models.Ticket(ticket_id=id, title=title, resolved=0, read=0, description=description, user=username)
				ticket.save()
				messages.add_message(request, messages.SUCCESS, 'Create Successful')
				return render(request, 'ticketcreation/creation.html')
		else:
			# user is superuser
			return HttpResponseForbidden()
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
			return render(request, 'ticketcreation/detail.html', {"item": item[0]})
		else:
			# user is normal user
			HttpResponseRedirect(reverse("home:index"))
	else:
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
			return render(request, 'ticketcreation/show.html', {"list": list})
		else:
			# user is normal user
			return HttpResponseRedirect(reverse("home:index"))
	else:
		return HttpResponseRedirect(reverse("login:index"))
