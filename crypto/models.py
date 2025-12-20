from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    discription = models.TextField()
    
    def __str__(self):
        return f"{self.id} - {self.title} - {self.discription}"


class About(models.Model):
    discription = models.TextField()
    
    def __str__(self):
        return f"{self.id} - {self.discription}"
      

class Ideals(models.Model):
    name = models.CharField(max_length=60)  # Rekebisha typo hapa
    ideal = models.TextField()
    
    def __str__(self):
        return f"{self.id} - {self.name} - {self.ideal}"