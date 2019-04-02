
#Testing with views is a little more complicated
#need to test more code paths: intial display, display after data validation has failed
#display after validation has suceeded. The good news is that we use the client
#for testing exactly the same way as we did for display views only

from ticket_creation.models import Ticket
from django.test import TestCase
from django.urls import reverse


from createuser.views import error_message_user_exist, error_message_empty_input

# class Ticket(models.Model):
#     ticket_id = models.CharField(max_length=30)
#     title = models.CharField(max_length=60)
#     resolved = models.IntegerField(default=0)
#     read = models.IntegerField(default=0)
#     description = models.CharField(max_length=256)
#     user = models.CharField(max_length=60)


class CreateTicketInstanceViewTest(TestCase):

    def setUp(self):
        # Create an existing Ticket
        test_ticket1 = Ticket.objects.create(ticket_id='testticket1', title='Help', resolved=0,
                                             read=0, description='Please help thanks', user='John')
        # test_user1.is_active = True
        test_ticket1.save()

    # Test for GET request
    def test_redirect_to_new_form(self):
        response = self.client.get(reverse('ticket_creation:create'))
        self.assertEqual(response.status_code, 302)
        # page is moved temporarily


    def test_message_after_sucessful_creation(self):
        response = self.client.post(reverse('ticket_creation:create'),
                                {'ticket_id': 'testticket1',
                                'title': 'Help', 'resolved':0,
                                'read':0,'description':'Please help thanks',
                                'user':'John'} )
        #messages.add_message(request, messages.SUCCESS, 'Create Successful')
        #self.assertTrue('Create Successful' in response.cookies['messages'].value)
        #since such ticket has been created, should create new message above Create Successful
        self.assertEqual(response.status_code,302)


    #Testing for POST request
    def test_redirect_if_username_taken(self):
        response = self.client.post(reverse('createuser:index'), {'username':'testuser1',
                                                                  'password':'Helloworld123',
                                                                  'email': 'test@test.com'})
        #since test_user1 already exist, no redirection remain on the same page
        self.assertTrue('error_message' in response.context)
        # Check that the right Error Message is displayed
        self.assertEqual(response.context['error_message'], error_message_user_exist)


    def test_submit_empty_form(self):
        response = self.client.post(reverse('createuser:index'),{'username':None,
                                                                  'password':None,
                                                                  'email':None} )
        self.assertTrue('error_message' in response.context)
        # Check that the right Error Message is displayed
        self.assertEqual(response.context['error_message'], error_message_empty_input)



    def test_form_invalid_password(self):
        response = self.client.post(reverse('createuser:index'), {'username': 'HappyDay1',
                                                                  'password': None,
                                                                  'email': 'test.test@gmail.com'})
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('createuser:index'))
        self.assertTrue('error_message' in response.context)
        # Check that the right Error Message is displayed
        self.assertEqual(response.context['error_message'], error_message_empty_input)


    def test_form_invalid_email(self):
        response = self.client.post(reverse('createuser:index'), {'username': 'HappyDay1',
                                                                  'password': 'passWord123',
                                                                  'email': None})
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('createuser:index'))
        self.assertTrue('error_message' in response.context)
        # Check that the right Error Message is displayed
        self.assertEqual(response.context['error_message'], error_message_empty_input)


    def test_uses_correct_template(self):
        response = self.client.get('/createuser/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'createuser/user.html')