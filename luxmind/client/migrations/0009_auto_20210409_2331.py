# Generated by Django 2.2.10 on 2021-04-09 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0008_auto_20210403_0808'),
    ]

    operations = [
        migrations.AddField(
            model_name='temppaper',
            name='PaperPref',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='temppaper',
            name='WriterPref',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
