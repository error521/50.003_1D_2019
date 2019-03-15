from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .forms import UserForm


@csrf_exempt
def get_user(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get('email')
		phoneNumber = request.POST.get('phoneNumber')

		user=User.objects.filter(username=username)

		if user.exists()==False:
			user = User.objects.create_user(username=username, email=email, password=password)
			user.is_active = True
			user.save()
			return HttpResponseRedirect(reverse("login:index"))
		else:
			# redirect back to the same page
			return HttpResponseRedirect(reverse("createuser:index"))

	# if a GET (or any other method) we'll create a blank form
	else:
		form = UserForm()

	return render(request, 'createuser/user.html')
