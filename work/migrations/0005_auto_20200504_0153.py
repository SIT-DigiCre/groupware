# Generated by Django 3.0.3 on 2020-05-03 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0006_delete_usertool'),
        ('work', '0004_auto_20200501_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='tools',
            field=models.ManyToManyField(blank=True, to='tool.Tool'),
        ),
    ]
