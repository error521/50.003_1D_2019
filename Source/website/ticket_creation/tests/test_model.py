from django.test import TestCase
from ticket_creation.models import Ticket
from django.urls import reverse
from ticket_creation.models import Ticket_Details
from ticket_creation.models import All_Tickets
import datetime
from django.apps import apps

# class Ticket(models.Model):
#     ticket_id = models.CharField(max_length=30)
#     title = models.CharField(max_length=60)
#     resolved = models.IntegerField(default=0)
#     read = models.IntegerField(default=0)
#     description = models.CharField(max_length=256)
#     user = models.CharField(max_length=60)
#
# class All_Tickets(models.Model):
#     # note: each model has its primary key, which increments as new elements are added, and the new number forms the element's id
#     size = models.IntegerField()  # represents number of replies in each ticket
#     creator = models.IntegerField()  # id of user
#     addressed_by = models.IntegerField(null=True, blank=True)  # id of admin
#     resolved_by = models.IntegerField(null=True, blank=True)  # if None, ticket is not resolved
#     read_by = models.CharField(max_length=100, null=True, blank=True)  # to have concaternated ids of admins (delimited by ",") that read the ticket to be concaternated to this value. I chose not to create new table as i needed to push for progress, otherwise that is defo prefered
#     queue_number = models.IntegerField()  # to be implemented in future
#     dateTime_created = models.DateTimeField()  # datetime object obtained with datetime.datetime.now()
#
# class Ticket_Details(models.Model):
#     # represent model that contains all replies and tickets
#     ticket_id = models.IntegerField()  # represent unique id of ticket in All_Tickets
#     thread_queue_number = models.IntegerField()  # in a thread (of replies under a ticket, queue number represents the order of replies, starting from 0 (the original ticket itself))
#     author = models.IntegerField()  # represent id of the user, stated in the table 'createuser_extended_user' in database 50003
#     title = models.CharField(max_length=60)
#     description = models.CharField(max_length=256)
#     image = models.ImageField(max_length=100, null=True, blank=True)  # to be implemented
#     file = models.FileField(null=True, blank=True)  # to be implemented
#     dateTime_created = models.DateTimeField()  # datetime object obtained with datetime.datetime.now()


class TicketCreationModelTest(TestCase):
    def setUp(self):
        test_ticket1 = Ticket.objects.create(ticket_id='testTicket1',
                              title='Help me',
                              resolved=0,
                              read=0,
                              description='I just want to finish this project',
                              user='testuser1')

        test_ticket1.save()

        test_ticket2 = Ticket.objects.create(ticket_id='testTicket2',
                              title='Ticket Creation not working',
                              resolved=0,
                              read=0,
                              description='Tried to create a ticket but gives error',
                              user='testuser2')

        test_ticket2.save()

    def test_ticket_fields(self):
        title_ticket1 = Ticket.objects.get(pk=1)
        self.assertEquals(title_ticket1.ticket_id,'testTicket1')
        self.assertEquals(title_ticket1.title, 'Help me')
        self.assertEquals(title_ticket1.resolved, 0)
        self.assertEquals(title_ticket1.read, 0)
        self.assertEquals(title_ticket1.description,
                          'I just want to finish this project')
        self.assertEquals(title_ticket1.user,'testuser1')
        title_ticket2 = Ticket.objects.get(pk=2)
        self.assertEquals(title_ticket2.ticket_id, 'testTicket2')
        self.assertEquals(title_ticket2.title, 'Ticket Creation not working')
        self.assertEquals(title_ticket2.resolved, 0)
        self.assertEquals(title_ticket2.read, 0)
        self.assertEquals(title_ticket2.description,
                          'Tried to create a ticket but gives error')
        self.assertEquals(title_ticket2.user, 'testuser2')

    def test_all_ticket_model(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        all_ticket = All_Tickets(size=1,creator=0,
                                 addressed_by=1,resolved_by=None,
                                 read_by=1,queue_number=1,
                                 dateTime_created=datetime.datetime.now())
        all_ticket.save()
        self.assertTrue(All_Tickets.objects.exists())


