# Generated by Django 2.2.2 on 2020-01-18 22:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20200118_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='age',
            field=models.CharField(choices=[('21', 'Adults'), ('6', 'Kids'), ('0', 'All'), ('16', 'Teenagers')], max_length=2),
        ),
        migrations.AlterField(
            model_name='movies',
            name='kind',
            field=models.CharField(choices=[('C', 'Comedy'), ('R', 'Romance'), ('D', 'Drama'), ('H', 'Horror'), ('T', 'Thriller'), ('F', 'Fantasty'), ('ScI', 'Science-Fiction')], max_length=3),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='ordered',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 1, 18, 23, 46, 50, 97370), null=True),
        ),
    ]
