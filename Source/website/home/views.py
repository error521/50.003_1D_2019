from audioop import reverse

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from createuser.models import Extended_User as User
from ticket_creation.views import sort_ticket_list
from ticket_creation.models import All_Tickets,Ticket, notification

def home(request):
	"""
	Used by admin and nonadmin. Displays all tickets for admin, and all tickets posted nonadmin for nonadmins
	"""

	error_message = None
	if (request.user.is_authenticated):
		# user is logged in
		if (request.user.is_superuser):
			# user is superuser
			username = request.user.get_username()
			ticketlist = len(All_Tickets.objects.all())
			unresolvedlist = len(All_Tickets.objects.all().filter(resolved_by=None))

			# count unread tickets - essentially check how many tickets is created by the user but does not have the user$
			unreadlist = 0
			for i in All_Tickets.objects.all():
				if i.read_by == None:  # no one has read the ticket yet
					unreadlist += 1
				elif str(request.user.id) not in i.read_by:  # someone has read it but its not the user
					unreadlist += 1

			notification_ticket = notification.objects.filter(type=0,creater_type=1)
			notification_msg = notification.objects.filter(type=1,creater_type=1)


			try:
				task = round((unresolvedlist / ticketlist)*100,2)
			except ZeroDivisionError:
				return render(request, 'noticketadmin.html' )

			outputList = sort_ticket_list(request, All_Tickets.objects.all(), request.user.is_superuser)
			return render(request, 'dashboardadmin.html', {"list": outputList,'error_message':error_message, 'ticket':ticketlist, "unresolved":unresolvedlist, "unread":unreadlist, 'task':task,"username":username, "new_ticket":notification_ticket,"new_msg":notification_msg, "numofnewticket":len(notification_ticket),"numofnewmsg":len(notification_msg)})

		else:
			# user is normal user

			username = request.user.id

			ticket_ids =[]

			ticketlist = All_Tickets.objects.all().filter(creator=username)

			for i in ticketlist:
				ticket_ids.append(i.id)


			notification_tickets = []
			notification_msgs = []

			notification_ticket = notification.objects.filter(type=0, creater_type=0)
			notification_msg = notification.objects.filter(type=1, creater_type=0)
			for i in notification_ticket:
				if i.ticket_id in ticket_ids:
					notification_tickets.append(i)
			for i in notification_msg:
				if i.ticket_id in ticket_ids:
					notification_msgs.append(i)



			unresolvedlist = len(All_Tickets.objects.all().filter(resolved_by=None, creator=username))

			# count unread tickets - essentially check how many tickets is created by the user but does not have the user's id in read_by
			unreadlist = 0
			for i in All_Tickets.objects.all().filter(creator=username):
				if i.read_by == None:  # no one has read the ticket yet
					unreadlist += 1
				elif str(request.user.id) not in i.read_by:  # someone has read it but its not the user
					unreadlist += 1

			if (len(ticketlist) == 0):
				return render(request, 'noticketuser.html' )
			print(request.user.email)
			outputList = sort_ticket_list(request, All_Tickets.objects.all().filter(creator=request.user.id),
				request.user.is_superuser)
			print(len(outputList))
			return render(request, 'dashboarduser.html', {'error_message':error_message,'username':request.user.get_username(), "list":outputList, 'ticket':len(ticketlist), "unresolved":unresolvedlist,'unread':unreadlist, "new_tickets":notification_tickets, "new_msg":notification_msgs,"numofnewticket":len(notification_tickets),"numofnewmsg":len(notification_msgs)})

	else:
		# user has not logged in, redirect to login page
		return HttpResponseRedirect(reverse('login:index'))

