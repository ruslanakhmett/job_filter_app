# Generated by Django 4.0.5 on 2022-07-17 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parsers_and_bot', '0005_alter_vacancy_for_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='global_users',
            old_name='name',
            new_name='user_name',
        ),
        migrations.RenameField(
            model_name='vacancy',
            old_name='tg_id',
            new_name='tg_chat_id',
        ),
        migrations.RenameField(
            model_name='vacancy',
            old_name='for_user',
            new_name='user_name',
        ),
        migrations.RenameField(
            model_name='vacancy',
            old_name='name',
            new_name='vac_name',
        ),
    ]
