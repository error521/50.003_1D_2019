
#Testing with views is a little more complicated
#need to test more code paths: intial display, display after data validation has failed
#display after validation has suceeded. The good news is that we use the client
#for testing exactly the same way as we did for display views only

from django.test import TestCase
from ticket_creation.models import Ticket
from django.urls import reverse
from django.test import Client
from createuser.models import Extended_User
from ticket_creation.views import error_message_invalid_input, \
    error_message_empty_input, error_message_success,\
    error_message_forbidden_administrator,\
    error_message_forbidden_nonadministrator,\
    error_message_one_checkbox,error_message_unauthorised,\
    error_message_unknown_error


# class Ticket(models.Model):
#     ticket_id = models.CharField(max_length=30)
#     title = models.CharField(max_length=60)
#     resolved = models.IntegerField(default=0)
#     read = models.IntegerField(default=0)
#     description = models.CharField(max_length=256)
#     user = models.CharField(max_length=60)


class CreateTicketInstanceViewTest(TestCase):
    @classmethod
    def setUp(self):
        self.client = Client()
        # Create an existing User
        test_user2 = Extended_User.objects.create(username='testuser2',
                                                  password='HelloSekai123',
                                                  email='testing@test.com',
                                                  phoneNumber='12345679',
                                                  notify_email=True,
                                                  notify_sms=False)
        test_user2.set_password('HelloSekai123')
        test_user2.is_active = True
        test_user2.save()
        test_ticket1 = Ticket.objects.create(ticket_id='testticket1',
                                             title='Help', resolved=0,
                                             read=0,
                                             description='Please help thanks',
                                             user='testuser2')
        test_ticket1.save()


    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('ticket_creation:create'))
        self.assertRedirects(response,'/login/')

    def test_logged_in_(self):
        login = self.client.login(username='testuser2',
                             password='HelloSekai123')
        print("Is user logged in")
        print(login)
        response = self.client.get(reverse('login:index'))
        print(response.context)
        self.assertTemplateUsed(response,'login/not_logged_in.html')
        self.assertEqual(response.status_code,200)
        self.assertTrue('error_message' in response.context)

    def test_home_page_status_code(self):
        response = self.client.get('/ticket_creation/')
        self.assertEquals(response.status_code, 302)

    def test_create_page_status_code(self):
        response = self.client.get(reverse('ticket_creation:create'))
        self.assertEquals(response.status_code, 302)

    def test_display_page_status_code(self):
        response = self.client.get(reverse('ticket_creation:display'))
        self.assertEquals(response.status_code, 302)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('ticket_creation:create'))
        self.assertEquals(response.status_code, 302)


    def test_SUCCESS_logged_in_create_ticket(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        response = self.client.post(reverse('ticket_creation:create'), {
                                                                        'title': 'Help',
                                                                        'email': 'testing@test.com',
                                                                        'description': 'Please help thanks',
                                                                        })
        print(response)
        print(response.context['error_message'])
        self.assertTrue(response.status_code,200)
        self.assertEqual(response.context["error_message"], error_message_success)

    def test_FAILURE_INVALID_TITLE_logged_in_create_ticket(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        response = self.client.post(reverse('ticket_creation:create'), {
                                                                        'title': '@Help',
                                                                        'email': 'testing@test.com',
                                                                        'description': 'Please help thanks',
                                                                        })
        print(response)
        print(response.context['error_message'])
        self.assertTrue(response.status_code,200)
        self.assertNotEqual(response.context["error_message"], error_message_success)

    def test_display_ticket(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        response = self.client.post(reverse('ticket_creation:create'), {
            'title': 'HelpAgain',
            'email': 'testing@test.com',
            'description': 'Please help again thanks',
        })
        response = self.client.get(reverse('ticket_creation:display'))