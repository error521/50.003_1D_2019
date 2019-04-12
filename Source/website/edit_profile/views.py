from django.shortcuts import render

from createuser.models import Extended_User


# Create your views here.
def index(request):
	"""
	For admins and non-admin, allows user to view current email, phone number, notification preferences,
	and can change email, phone number, notiifcation preferences, and password.
	"""
	error_message = None

	if request.method == 'POST':
		pass
	else:
		user_information = {'username':None, 'email':None, 'phoneNumber':None}
		return render(request, 'edit_profile/index.html', {'error_message':error_message})
