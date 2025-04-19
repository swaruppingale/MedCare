from django.urls import path
from . import views

urlpatterns = [
    path('symptoms/', views.reply_whatsapp)
]