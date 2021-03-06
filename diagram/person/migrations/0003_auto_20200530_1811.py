# Generated by Django 3.0.5 on 2020-05-30 15:11

import diagram.person.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_auto_20200428_0115'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'Персона', 'verbose_name_plural': 'Персоны'},
        ),
        migrations.AlterModelOptions(
            name='settings',
            options={'verbose_name': 'Настройки пользователя', 'verbose_name_plural': 'Настройки пользователей'},
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', diagram.person.models.CustomUserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='is_email_verify',
            field=models.BooleanField(default=False, verbose_name='Email подтвержден'),
        ),
        migrations.AlterField(
            model_name='person',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='person',
            name='native_lang',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Родной язык'),
        ),
        migrations.AlterField(
            model_name='person',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='person', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='username'),
        ),
    ]
