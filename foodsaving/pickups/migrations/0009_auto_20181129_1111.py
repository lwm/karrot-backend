# Generated by Django 2.1.2 on 2018-11-29 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pickups', '0008_auto_20181124_1406'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pickupdate',
            old_name='done_and_processed',
            new_name='feedback_possible',
        ),
    ]
