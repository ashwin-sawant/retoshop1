from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)  # Explicit user ID
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # For hashed passwords

    def __str__(self):
        return f"{self.first_name} {self.last_name}"