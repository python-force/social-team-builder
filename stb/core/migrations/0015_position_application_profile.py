# Generated by Django 2.2 on 2019-04-18 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20190417_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='position_application',
            name='profile',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, to='core.Profile'),
            preserve_default=False,
        ),
    ]
