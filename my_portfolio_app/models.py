from django.db import models

# Create your models here.
class Projects(models.Model):
    image = models.ImageField(upload_to='projects_images')
    title = models.CharField(max_length=100)
    para = models.CharField(max_length=255)
    link = models.CharField(max_length=255)

    def __str__(self):
        return self.title


