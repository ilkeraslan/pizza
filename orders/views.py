from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .forms import NameForm

from .models import Pizza, Size, Topping


class IndexView(generic.ListView):

    # Use existing template
    template_name = 'orders/index.html'

    # Pass context object
    context_object_name = 'menu_list'

    def get_queryset(self):
        return Pizza.objects.all()


class DetailView(generic.DetailView):

    # Which model to use
    model = Pizza

    # Use existing template
    template_name = 'orders/detail.html'

    # Override get_context_data() method to add extra content to DetailView
    # https://docs.djangoproject.com/en/2.1/topics/class-based-views/generic-display/#adding-extra-context
    def get_context_data(self, **kwargs):

        # Call the base implementation
        context = super().get_context_data(**kwargs)

        # Add in a QuerySet of all the sizes and toppings
        context['size_list'] = Size.objects.all()
        context['topping_list'] = Topping.objects.all()

        return context

    def get_queryset(self):
        return Pizza.objects.all()


def login_view(request):
    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            print(user)

        # username = request.POST['username']
        # password = request.POST['password']
        # user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # Redirect to index
                return HttpResponseRedirect(reverse('orders:index'))
    form = NameForm()
    return render(request, 'registration/login.html', {'form': form})
