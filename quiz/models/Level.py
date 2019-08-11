from django.db import models

class Level(models.Model):
    level_number = models.IntegerField(default=1)
    start_time = models.DateTimeField(blank=True)
    end_time = models.DateTimeField(blank=True)

    def __str__(self):
        return self.level_number