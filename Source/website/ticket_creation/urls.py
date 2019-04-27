from django.urls import path

from . import views

app_name = 'ticket_creation'
urlpatterns = [
    path('', views.create, name='create'),  # creating ticket
    path('display/', views.list, name='display'),  # listing out all tickets
    path('delete/', views.delete, name='delete'),  # deleting tickets
    path('detail/', views.detail, name='detail'),  # display detail of tickets/reply to tickets
    path('resolve/', views.resolve, name='resolve'),  # resolving tickets
    path('selected_list/', views.selected_list, name='selected_list'),  # display nonadmin user's tickets only, or admin user's tickets only
    path('viewUnread/', views.viewUnread, name='unread'),  # display all unread tickets
    path('viewUnresolve/', views.viewUnresolved, name='unresolve'),  # display all unresolved tickets
]
