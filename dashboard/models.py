from django.db import models

class Dataset(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='datasets/')
    file_type = models.CharField(max_length=10)


    def __str__(self):
        return self.name