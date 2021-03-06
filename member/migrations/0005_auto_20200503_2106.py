# Generated by Django 3.0.3 on 2020-05-03 12:06
from django.core.management import call_command
from django.db import migrations, models

def load_fixture(apps, schema_editor):
        call_command('loaddata', 'member/fixture/init.json', app_label='member')
class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_profile_intro'),
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='divisions',
            field=models.ManyToManyField(to='member.Division'),
        ),
        migrations.RunPython(load_fixture),
    ]