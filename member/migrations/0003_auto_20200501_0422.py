# Generated by Django 3.0.3 on 2020-04-30 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_usertool'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='generation',
            field=models.IntegerField(blank=True),
        ),
    ]
