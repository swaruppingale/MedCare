from django.contrib import admin
from .models import twilioModel, AISummaryModel

# Registering models so that can see it in Django Admin
admin.site.register(twilioModel)
admin.site.register(AISummaryModel)