# Generated by Django 2.2 on 2019-04-11 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20190411_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='core.Project'),
        ),
    ]
