# Generated by Django 2.2 on 2019-04-13 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20190411_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', related_query_name='projects', to='core.Project'),
        ),
    ]
