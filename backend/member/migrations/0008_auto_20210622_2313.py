# Generated by Django 3.0.3 on 2021-06-22 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0007_auto_20210622_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='message',
            field=models.CharField(max_length=140, verbose_name='ひとこと'),
        ),
    ]
