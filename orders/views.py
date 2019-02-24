from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Pizza


class IndexView(generic.ListView):

    # Use existing template
    template_name = 'orders/index.html'

    # Pass context object
    context_object_name = 'menu_list'

    def get_queryset(self):
        return Pizza.objects.all()
