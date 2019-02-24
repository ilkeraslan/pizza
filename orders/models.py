from django.db import models


class Pizza(models.Model):
    pizza_name = models.CharField(max_length=25)
    pizza_type = models.CharField(max_length=25)
    pizza_description = models.CharField(max_length=200)
    pizza_price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.pizza_name} ({self.pizza_type}) -- {self.pizza_description}"


class Size(models.Model):
    size_text = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.size_text}"


class Topping(models.Model):
    topping_text = models.CharField(max_length=25)
    topping_price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.topping_text} ({self.topping_price} €)"
