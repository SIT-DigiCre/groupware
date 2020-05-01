# Generated by Django 3.0.3 on 2020-04-28 08:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bbs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stamp',
            name='img_url',
        ),
        migrations.AddField(
            model_name='stamp',
            name='image',
            field=models.ImageField(default='defo', upload_to='stamp_img/'),
        ),
        migrations.CreateModel(
            name='ReplyStamp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs.Reply')),
                ('stamp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs.Stamp')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MessageStamp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs.Message')),
                ('stamp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs.Stamp')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
