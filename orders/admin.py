from django.contrib import admin

from .models import Pizza


class PizzaAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Pizza information', {'fields': ['pizza_name', 'pizza_type', 'pizza_description']}),
        ('Pizza price', {'fields': ['pizza_price']})
    ]

    # Use list_display, a tuple of field names to display as columns
    list_display = ('pizza_name', 'pizza_type', 'pizza_description')

    # Use list filter to add a sidebar to filter
    list_filter = ['pizza_type']

    # Add a search box to search question texts, uses LIKE query
    search_fields = ['pizza_name', 'pizza_description']


admin.site.register(Pizza, PizzaAdmin)
