# Generated by Django 3.1.2 on 2020-10-11 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
        ('instructor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('duration', models.FloatField()),
                ('paid', models.BooleanField(blank=True, default=False, null=True)),
                ('status', models.CharField(blank=True, max_length=30, null=True)),
                ('equipment', models.CharField(blank=True, max_length=30, null=True)),
                ('kite_brand', models.CharField(blank=True, max_length=30, null=True)),
                ('kite_size', models.FloatField(blank=True, null=True)),
                ('board', models.CharField(blank=True, max_length=30, null=True)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
                ('in_progress', models.BooleanField(blank=True, default=False, null=True)),
                ('instructor', models.ManyToManyField(related_name='lessons', to='instructor.Instructor')),
                ('student', models.ManyToManyField(related_name='lessons', to='student.Student')),
            ],
        ),
    ]
