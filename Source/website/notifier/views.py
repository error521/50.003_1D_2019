from django.shortcuts import render
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect

# def send_email(request):
#     subject = request.POST.get('subject', '')
#     message = request.POST.get('message', '')
#     from_email = request.POST.get('from_email', '')
#     if subject and message and from_email:
#         try:
#             send_mail(subject, message, from_email, ['admin@example.com'])
#         except BadHeaderError:
#             return HttpResponse('Invalid header found.')
#         return HttpResponseRedirect('/contact/thanks/')
#     else:
#         # In reality we'd use a form class
#         # to get proper validation errors.
#         return HttpResponse('Make sure all fields are entered and valid.')

from django.conf import settings
from twilio.rest import TwilioRestClient
from django.template.loader import render_to_string

def send_sms(to, message, content={}, template=None):
    '''sms utility method'''

    content.update({
    'put any content here'
    })

    if not template:
        '''If we have a template format the message'''
        message = render_to_string(template, content)
        message = message.encode('utf-8')
    client = TwilioRestClient(
        settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    response = client.messages.create(
        body=message, to=to, from_='+15556667777')
    return response

# def downtime_monitor():
# 	content = {'when':timezone.now(),'name':user.name,'back_up':back_up}
# 	message = ''
# 	template = 'downtime_alert.html'
#     to = user.phonenumber
# 	response = send_sms(to, message, content, template)
# 	#do something with response