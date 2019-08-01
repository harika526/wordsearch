from django.db import models
from django.db.models.functions import Length

# Create your models here.


class Words(models.Model):
    word = models.CharField(max_length=200)
    usage_count = models.BigIntegerField()

    class Meta:
        ordering = ['-usage_count', 'word', Length('word')]

    def __str__(self):
        return self.word
