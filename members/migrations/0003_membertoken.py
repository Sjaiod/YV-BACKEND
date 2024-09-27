# Generated by Django 5.0.7 on 2024-09-26 14:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_remove_member_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberToken',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='member_auth_token', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
