# Generated by Django 3.1.2 on 2020-12-06 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_auto_20201130_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='weight',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]