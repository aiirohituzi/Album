from django.db import models

class photo(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=200)
    path = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)