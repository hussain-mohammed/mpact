# Generated by Django 2.2 on 2020-12-24 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mpact', '0004_auto_20201222_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='chat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bot', to='mpact.Chat'),
        ),
    ]