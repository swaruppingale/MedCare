from django.db import models

class twilioModel(models.Model):
    profileName = models.CharField(verbose_name="Profile Name", max_length=100)
    WaID = models.CharField(verbose_name="Whatsapp ID", max_length=15)
    message = models.TextField(verbose_name="Message")

class AISummaryModel(models.Model):
    WaID = models.CharField(verbose_name="Whatsapp ID", max_length=15)
    profileName = models.CharField(verbose_name="Profile Name", max_length=100)
    summary = models.TextField(verbose_name="AI Summary")
