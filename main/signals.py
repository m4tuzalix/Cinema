from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import Movies, Movie_dates, Hours, Dates
from datetime import datetime, timedelta


@receiver(post_save, sender=Movies)
def create_movie_dates(sender, instance, created, **kwargs):
    if created:
        all_hours = Hours.objects.all()
        new_schedule = Movie_dates.objects.create(main_movie=instance)
        for x in range(7):
            date = datetime.now() + timedelta(days=x)
            new_date = Dates.objects.create(movie=instance, date=date)
            new_date.save()
            new_schedule.dates.add(new_date)
            for h in all_hours:
                new_schedule.time.add(h)
            new_schedule.save()



