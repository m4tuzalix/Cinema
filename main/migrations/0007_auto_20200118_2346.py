# Generated by Django 2.2.2 on 2020-01-18 22:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20200118_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='age',
            field=models.CharField(choices=[('6', 'Kids'), ('0', 'All'), ('16', 'Teenagers'), ('21', 'Adults')], max_length=2),
        ),
        migrations.AlterField(
            model_name='movies',
            name='kind',
            field=models.CharField(choices=[('R', 'Romance'), ('D', 'Drama'), ('T', 'Thriller'), ('F', 'Fantasty'), ('ScI', 'Science-Fiction'), ('H', 'Horror'), ('C', 'Comedy')], max_length=3),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='ordered',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 1, 18, 23, 46, 45, 450471), null=True),
        ),
    ]
