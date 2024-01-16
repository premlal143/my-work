from django.urls import path
from .views import *

urlpatterns =[
    path('',login_view, name='login_view'),
    path('register_request_view/',register_request_view, name='register_request_view'),
    path('forgot_password_view/',forgot_password_view, name='forgot_password_view'),
    path('otp_verify_view/', otp_verify_view, name='otp_verify_view'),
    path('logout/', logout, name='logout'),

    path('dashboard_view/',dashboard_view, name ='dashboard_view'),
    path('tasks_view/', tasks_view, name='tasks_view'),
    path('update_task/<str:task_id>', update_task, name='update_task'),
    path('delete_task/<str:task_id>', delete_task, name='delete_task'),
    path('payment_entry/<str:task_id>', payment_entry, name='payment_entry'),
    path('parties_view/', parties_view, name='parties_view'),
    path('update_party_details/<int:id>',update_party_details, name = 'update_party_details' ),
    path('delete_party/<int:id>', delete_party, name = 'delete_party'),
    path('payments_view/', payments_view, name='payments_view'),
    path('profile_view/', profile_view, name='profile_view'),
]