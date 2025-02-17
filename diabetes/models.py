from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    diabetes_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
