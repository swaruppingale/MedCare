from django.urls import path
from . import views

urlpatterns = [
    path("chatbot", views.chatbot_page, name="chatbot_page"),
    path("chatbot/upload_and_query", views.upload_and_query, name="upload_and_query"),
]