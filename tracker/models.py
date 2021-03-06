from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.

class Show(models.Model):
    show_id = models.AutoField(primary_key=True)
    show_name = models.CharField(max_length=100)
    picture_url = models.TextField(blank=True, null=True)
    # do I use datefield instead?
    year = models.CharField(max_length=10, blank=True, null=True)
    kind = models.CharField(max_length=10, null=True, default=None)
    overview = models.TextField(blank=True, null=True)
    service = ArrayField(models.CharField(max_length=30))

    def __str__(self):
        return self.show_name


class UserShowList(models.Model):
    user = models.ForeignKey('user_auth.User', related_name='user_shows', on_delete=models.SET_NULL, null=True)
    show = models.ForeignKey('Show', related_name='user_shows', on_delete=models.SET_NULL, null=True, blank=True)
    date_added = models.DateTimeField(verbose_name='date added', auto_now_add=True)

    class Meta:
        ordering = ('date_added', )
