# Generated by Django 3.0.2 on 2020-01-13 22:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mentorski', '0003_korisnici_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Predmeti',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ime', models.CharField(max_length=255)),
                ('kod', models.CharField(max_length=16)),
                ('program', models.TextField()),
                ('bodovi', models.IntegerField(max_length=11)),
                ('sem_redovni', models.IntegerField(max_length=11)),
                ('sem_izvanredni', models.IntegerField(max_length=11)),
                ('izborni', models.CharField(choices=[('da', 'Ne'), ('ne', 'Ne')], default='ne', max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='korisnici',
            name='status',
            field=models.CharField(choices=[('None', 'None'), ('Redovni', 'Redovni'), ('Izvanredni', 'Izvanredni')], default='Redovni', max_length=10),
        ),
        migrations.CreateModel(
            name='Upisi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=64)),
                ('predmet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorski.Predmeti')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('student', 'predmet')},
            },
        ),
        migrations.AddField(
            model_name='korisnici',
            name='upisni',
            field=models.ManyToManyField(through='mentorski.Upisi', to='mentorski.Predmeti'),
        ),
    ]
