# Generated by Django 2.2.3 on 2020-03-05 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20200305_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='age',
            field=models.CharField(choices=[('16', 'Teenagers'), ('6', 'Kids'), ('21', 'Adults'), ('0', 'All')], max_length=2),
        ),
        migrations.AlterField(
            model_name='movies',
            name='kind',
            field=models.CharField(choices=[('R', 'Romance'), ('H', 'Horror'), ('ScI', 'Science-Fiction'), ('F', 'Fantasty'), ('C', 'Comedy'), ('D', 'Drama'), ('T', 'Thriller')], max_length=3),
        ),
        migrations.AlterField(
            model_name='user_seats',
            name='ordered',
            field=models.DateTimeField(blank=True, default='2020-03-05 18:22', null=True),
        ),
    ]