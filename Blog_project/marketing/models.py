from django.db import models

class SignUp(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "SignUp's"

    def __str__(self):
        return self.email
