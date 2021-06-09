# Generated by Django 2.2.10 on 2021-04-09 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0009_auto_20210409_2331'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Document', models.ImageField(upload_to='images/%Y/%M/%D/')),
                ('ipaddress', models.CharField(max_length=100)),
                ('PaperId', models.CharField(blank=True, max_length=100)),
                ('UserId', models.CharField(blank=True, max_length=100)),
                ('PaperType', models.CharField(blank=True, max_length=100)),
                ('createdAt', models.DateField(auto_now_add=True)),
                ('updatedAt', models.DateField(auto_now=True)),
            ],
        ),
    ]
