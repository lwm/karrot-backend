# Generated by Django 2.1.2 on 2018-12-09 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0032_auto_20181209_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='deleted',
        ),
    ]