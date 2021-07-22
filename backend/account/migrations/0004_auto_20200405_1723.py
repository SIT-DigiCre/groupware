# Generated by Django 3.0.3 on 2020-04-05 08:23
from django.core.management import call_command
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200404_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='icon',
            field=models.ImageField(default='defo', upload_to='user_icon/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=True, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
        
    ]