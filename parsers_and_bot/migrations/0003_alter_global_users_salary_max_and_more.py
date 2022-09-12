# Generated by Django 4.0.5 on 2022-07-17 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parsers_and_bot', '0002_alter_global_users_start_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='global_users',
            name='salary_max',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='global_users',
            name='salary_min',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='for_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parsers_and_bot.global_users'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='tg_id',
            field=models.IntegerField(default=0),
        ),
    ]
