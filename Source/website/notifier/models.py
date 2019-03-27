# from django.db import models
# from django.contrib.auth import settings
#
#
# # Create your models here.
# NOTIFICATION_TARGET = (
#     ('1', 'User'),
#     ('2', 'EMPLOYEE'),
#     ('3', 'BOSS')
# )
#
#
# class Notification(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              on_delete=models.CASCADE,
#                              related_name='notification')
#     actor = models.CharField(max_length=50)
#     verb = models.CharField(max_length=50)
#     action = models.CharField(max_length=50, blank=True)
#     target = models.CharField(
#         max_length=1, default='1', choices=NOTIFICATION_TARGET)
#     description = models.TextField(blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#
# def __str__(self):
#     return f"{self.actor} {self.verb} {self.action} {self.target} at 			{self.timestamp}"