from django.db import models


class ContactDetails(models.Model):
   
    name = models.CharField(max_length=70, primary_key=True)
    phone_number = models.CharField(max_length=10, null=False)

    def __str__(self):
        return "{} - {}".format(self.name, self.phone_number)