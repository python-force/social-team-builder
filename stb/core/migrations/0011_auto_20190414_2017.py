# Generated by Django 2.2 on 2019-04-14 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20190414_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='profile',
            field=models.ManyToManyField(blank=True, related_name='skills', to='core.Profile'),
        ),
    ]
