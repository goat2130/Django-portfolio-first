# Generated by Django 4.2 on 2023-05-22 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_alter_profile_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='followers_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]