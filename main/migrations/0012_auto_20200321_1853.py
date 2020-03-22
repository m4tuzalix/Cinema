# Generated by Django 2.2.2 on 2020-03-21 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20200321_1850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dates',
            name='test',
        ),
        migrations.AlterField(
            model_name='movies',
            name='age',
            field=models.CharField(choices=[('16', 'Teenagers'), ('0', 'All'), ('21', 'Adults'), ('6', 'Kids')], max_length=2),
        ),
        migrations.AlterField(
            model_name='movies',
            name='kind',
            field=models.CharField(choices=[('F', 'Fantasty'), ('C', 'Comedy'), ('D', 'Drama'), ('ScI', 'Science-Fiction'), ('T', 'Thriller'), ('H', 'Horror'), ('R', 'Romance')], max_length=3),
        ),
        migrations.AlterField(
            model_name='seats',
            name='ordered',
            field=models.DateTimeField(blank=True, default='2020-03-21 18:53', null=True),
        ),
        migrations.AlterField(
            model_name='user_seats',
            name='ordered',
            field=models.DateTimeField(blank=True, default='2020-03-21 18:53', null=True),
        ),
    ]
