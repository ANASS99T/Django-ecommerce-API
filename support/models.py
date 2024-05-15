from django.db import models
from user.models import User

class Support(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    # add any additional fields here