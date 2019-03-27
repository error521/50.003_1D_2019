from audioop import reverse

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User

def home(request):
        error_message = None

        if (request.user.is_authenticated):
                # user is logged in
                if (request.user.is_superuser):
                        # user is superuser
	                return render(request, 'home/index_admin.html', {'error_message':error_message})
                else:
                        # user is normal user
	                return render(request, 'home/index_user.html', {'error_message':error_message})

        else:
                # user has not logged in, redirect to login page
                return HttpResponseRedirect(reverse('login:index'))

