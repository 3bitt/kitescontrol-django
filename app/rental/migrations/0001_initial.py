# Generated by Django 3.2.5 on 2021-08-11 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('paid', models.BooleanField(blank=True, default=False, null=True)),
                ('paid_date', models.DateTimeField(blank=True, null=True)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='student.student')),
            ],
        ),
        migrations.CreateModel(
            name='RentalDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(choices=[(None, 'UNKNOWN'), ('WETSUIT', 'Pianka'), ('HELMET', 'Kask'), ('LIFE_JACKET', 'Kamizelka ratunkowa'), ('HARNESS', 'Trapez'), ('LEASH', 'Leash'), ('BOARD', 'Deska'), ('KITE', 'Kite')], max_length=12)),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('rental', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental.rental')),
            ],
        ),
    ]