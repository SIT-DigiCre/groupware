# Generated by Django 3.0.3 on 2020-03-28 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ringi', '0004_auto_20200328_1913'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ('order',)},
        ),
    ]
