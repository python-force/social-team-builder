# Generated by Django 2.2 on 2019-04-25 20:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_profile_other_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
