# Generated by Django 3.0.3 on 2021-09-21 09:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0007_auto_20200521_0031'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('storage', '0001_initial'),
        ('work', '0006_auto_20200521_0031'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('intro', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='WorkItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('intro', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('files', models.ManyToManyField(to='storage.FileObject')),
                ('tags', models.ManyToManyField(blank=True, to='work.WorkTag')),
                ('tools', models.ManyToManyField(blank=True, to='tool.Tool')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]