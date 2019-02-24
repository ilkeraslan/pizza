from django.db import models


class Pizza(models.Model):
    pizza_name = models.CharField(max_length=25)
    pizza_type = models.CharField(max_length=25)
    pizza_description = models.CharField(max_length=200)
    pizza_price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.pizza_name} ({self.pizza_type}) -- {self.pizza_description}"
