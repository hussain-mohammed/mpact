# Generated by Django 2.2 on 2020-12-08 14:41

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mpact.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Phone number is invalid.', regex='^\\+?1?\\d{9,15}$'), mpact.models.validate_phone])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
