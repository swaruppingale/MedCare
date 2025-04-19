# Generated by Django 5.1.7 on 2025-03-16 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AISummaryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('WaID', models.CharField(max_length=15, verbose_name='Whatsapp ID')),
                ('profileName', models.CharField(max_length=100, verbose_name='Profile Name')),
                ('summary', models.TextField(verbose_name='AI Summary')),
            ],
        ),
        migrations.CreateModel(
            name='twilioModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profileName', models.CharField(max_length=100, verbose_name='Profile Name')),
                ('WaID', models.CharField(max_length=15, verbose_name='Whatsapp ID')),
                ('message', models.TextField(verbose_name='Message')),
            ],
        ),
    ]
