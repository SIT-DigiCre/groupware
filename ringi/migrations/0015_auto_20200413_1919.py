# Generated by Django 3.0.5 on 2020-04-13 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ringi', '0014_ringi_receipt_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ringi',
            name='receipt_image',
            field=models.ImageField(default='defo', upload_to='receipt_image/', verbose_name='領収書'),
        ),
    ]
