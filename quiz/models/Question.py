from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    answer_text =  models.CharField(max_length=200)
    hint = models.CharField(max_length=200,blank=True)
    image = models.ImageField(upload_to='images',default="Not Available", blank=True)
    audio = models.FileField(upload_to='audios',default="Not Available", blank=True)
    
    def __str__(self):
        return self.question_text