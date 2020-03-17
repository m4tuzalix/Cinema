# Generated by Django 2.2.3 on 2020-03-05 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20200305_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='seats',
            name='ordered',
            field=models.DateTimeField(blank=True, default='2020-03-05 18:36', null=True),
        ),
        migrations.AlterField(
            model_name='movies',
            name='age',
            field=models.CharField(choices=[('6', 'Kids'), ('16', 'Teenagers'), ('21', 'Adults'), ('0', 'All')], max_length=2),
        ),
        migrations.AlterField(
            model_name='movies',
            name='kind',
            field=models.CharField(choices=[('R', 'Romance'), ('ScI', 'Science-Fiction'), ('H', 'Horror'), ('D', 'Drama'), ('C', 'Comedy'), ('T', 'Thriller'), ('F', 'Fantasty')], max_length=3),
        ),
        migrations.AlterField(
            model_name='user_seats',
            name='ordered',
            field=models.DateTimeField(blank=True, default='2020-03-05 18:36', null=True),
        ),
    ]