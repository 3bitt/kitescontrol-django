# Generated by Django 3.1.2 on 2020-11-19 18:25

from django.db import migrations, models
import student.validators


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_auto_20201028_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='mobile_number',
            field=models.CharField(max_length=20, null=True, validators=[student.validators.validate_mobile]),
        ),
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=30, validators=[student.validators.validate_name]),
        ),
        migrations.AlterField(
            model_name='student',
            name='surname',
            field=models.CharField(max_length=30, validators=[student.validators.validate_name]),
        ),
    ]
