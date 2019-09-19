from django.contrib import admin

from .models import Cart, Pizza, Size, Topping


class PizzaAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Pizza information', {'fields': ['pizza_name', 'pizza_type', 'pizza_description']}),
        ('Pizza price', {'fields': ['pizza_price']})
    ]

    # Use list_display, a tuple of field names to display as columns
    list_display = ('pizza_name', 'pizza_type', 'pizza_description')

    # Use list filter to add a sidebar to filter
    list_filter = ['pizza_type']

    # Add a search box to search pizza names and descriptions, uses LIKE query
    search_fields = ['pizza_name', 'pizza_description']


class ToppingAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Topping information', {'fields': ['topping_text']}),
        ('Topping price', {'fields': ['topping_price']})
    ]

    # Use list_display, a tuple of field names to display as columns
    list_display = ('topping_text', 'topping_price')

    # Use list filter to add a sidebar to filter
    list_filter = ['topping_price']

    # Add a search box to search topping texts
    search_fields = ['topping_text']


class CartAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Cart information', {'fields': ['user', 'pizza_count', 'total']}),
        ('Cart total', {'fields': ['pizza_total', 'topping_total']})
    ]

    # Use list_display, a tuple of field names to display as columns
    list_display = ('user', 'pizza_count', 'total')

    # Use list filter to add a sidebar to filter
    list_filter = ['user']

    # Add a search box to search topping texts
    search_fields = ['user']


admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Size)
admin.site.register(Topping, ToppingAdmin)
admin.site.register(Cart, CartAdmin)
