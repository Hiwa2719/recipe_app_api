# Generated by Django 3.2 on 2021-04-11 04:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_user_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='dated_joined',
            new_name='date_joined',
        ),
    ]
