from django.urls import path

from . import views

urlpatterns = [
    path('',views.chatbot_interface, name='chatbot_interface'),
   
    # Ajoutez d'autres URL au besoin
]


