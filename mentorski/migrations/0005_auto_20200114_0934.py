# Generated by Django 3.0.2 on 2020-01-14 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorski', '0004_auto_20200113_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predmeti',
            name='izborni',
            field=models.CharField(choices=[('Ne', 'Ne'), ('Da', 'Da')], default='Da', max_length=10),
        ),
    ]
