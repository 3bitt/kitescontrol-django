# Generated by Django 3.1.2 on 2020-12-08 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_auto_20201208_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='wetsuit_size',
            field=models.CharField(blank=True, choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('S-128', 'S-128'), ('M-140', 'M-140'), ('L-146', 'L-146'), ('XL-152', 'XL-152')], max_length=6, null=True),
        ),
    ]
