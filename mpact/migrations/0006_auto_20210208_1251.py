# Generated by Django 2.2.17 on 2021-02-08 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpact', '0005_flaggedmessage_group_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='flaggedmessage',
            unique_together={('room_id', 'message_id')},
        ),
    ]