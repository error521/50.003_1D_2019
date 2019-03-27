from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse



@csrf_exempt
def view_profile(request):
    if (request.user.is_authenticated):
        email = request.user.email
        print(email)
        #phoneNo = request.user.phoneNumber
        username = request.user.username
        line = [email,username]
        return render(request, "viewProfile.html", {"line": line})
    else:
        return HttpResponseRedirect(reverse("login:index"))




def update_profile(request):
    if (request.user.is_authenticated):
        # user is logged in
        if request.method == 'POST':
            username = request.user.username
            email = request.user.email
            phone = request.POST.get('email')
            description = request.POST.get('description')
            print(username)
            ticket = models.Ticket(ticket_id=id, title=title, resolved=0, read=0, description=description,
                                   user=username)
            ticket.save()
        return render(request, 'ticketcreation/creation.html')
    else:
        return HttpResponseRedirect(reverse("login:index"))