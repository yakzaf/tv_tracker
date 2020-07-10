from django.db import models
from django.utils import timezone


# Create your models here.

# class Shows(models.Model):
#     show_id = models.AutoField(primary_key=True)
#     show_name = models.CharField(max_length=100)
#     picture_url = models.TextField()
#     service = models.CharField(max_length=20)
#
# class UsersShows(models.Model):
#     user_id = models.IntegerField(null=False)
#     show_id = models.IntegerField(null=False)
#     update_time = models.DateTimeField(default=timezone.now)
#     user = models.ManyToManyField(Accounts)
#     show = models.ManyToManyField(Shows)
