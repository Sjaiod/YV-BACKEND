# Generated by Django 5.0.7 on 2024-10-11 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_alter_member_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='profile_pic',
            field=models.CharField(blank=True, default='profilepic', max_length=255, null=True),
        ),
    ]
