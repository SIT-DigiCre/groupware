# Generated by Django 3.0.3 on 2020-04-14 15:58
from django.core.management import call_command
from django.db import migrations, models

def load_fixture(apps, schema_editor):
        call_command('loaddata', 'account/fixture/init.json', app_label='account')
class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200405_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='icon',
            field=models.ImageField(default='defo.png', upload_to='user_icon/'),
        ),
        
        migrations.AddField(
            model_name='user',
            name='is_leaders',
            field=models.BooleanField(default=False, help_text='アカウントの追加処理などへのアクセス', verbose_name='leaders status'),
        ),
        migrations.AddField(
            model_name='user',
            name='student_id',
            field=models.CharField(blank=True, max_length=7),
        ),
        migrations.RunPython(load_fixture),
    ]
