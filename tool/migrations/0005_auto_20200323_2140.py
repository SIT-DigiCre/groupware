# Generated by Django 3.0.3 on 2020-03-23 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0004_auto_20200323_2114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tool',
            name='tool_icon',
        ),
        migrations.AddField(
            model_name='tool',
            name='icon',
            field=models.ImageField(default='defo', upload_to='tool_icon/'),
        ),
    ]
