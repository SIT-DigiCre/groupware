# Generated by Django 3.0.3 on 2020-04-14 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ringi', '0015_auto_20200413_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ringi',
            name='urgency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ringi.Urgency', verbose_name='緊急度'),
        ),
    ]
