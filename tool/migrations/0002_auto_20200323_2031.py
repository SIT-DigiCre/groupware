# Generated by Django 3.0.3 on 2020-03-23 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tool',
            name='tool_icon',
            field=models.ImageField(upload_to='tool_icon/'),
        ),
    ]
