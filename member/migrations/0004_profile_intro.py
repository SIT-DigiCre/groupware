# Generated by Django 3.0.3 on 2020-04-30 20:20

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_auto_20200501_0422'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='intro',
            field=markdownx.models.MarkdownxField(blank=True, verbose_name='intro'),
        ),
    ]
