# Generated by Django 2.2.10 on 2021-05-04 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0017_temppaper_bidoption'),
    ]

    operations = [
        migrations.AddField(
            model_name='temppaper',
            name='CPP',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='temppaper',
            name='ENL',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='temppaper',
            name='ESL',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
