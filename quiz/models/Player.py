from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=200,blank=True)
    email = models.CharField(max_length=200)
    score = models.IntegerField(default=0)
    submit_time =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name