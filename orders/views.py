import requests
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .forms import CustomLoginForm, SignupForm

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
        form = CustomLoginForm(data=request.POST)

        if not is_recaptcha_valid(request):
            messages.error(request, "Invalid recaptcha.")
            return render(request, 'registration/login.html', {'form': CustomLoginForm()})

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            print(user)

            if user is not None:
                login(request, user)

                # Redirect to index
                messages.success(request, "Logged in.")
                return HttpResponseRedirect(reverse('orders:index'))
            else:
                messages.error(request, "Invalid credentials.")
        else:
            messages.error(request, "Invalid form submission.")
            return render(request, 'registration/login.html', {'form': CustomLoginForm()})

    else:
            form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():

            # Save the user into database
            form.save()

            # Get the corresponding fields from the submitted form
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']

            # Authenticate the user
            user = authenticate(username=username, password=raw_password)

            # Login the user
            if user is not None:
                login(request, user)

                # Redirect to home
                messages.success(request, "Signed up.")
                return HttpResponseRedirect(reverse('orders:index'))

            else:
                # Error message
                messages.error(request, "User already exists.")

    else:
            form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def is_recaptcha_valid(request):
    """
    Verify if the response for the Google recaptcha is valid.
    """
    return requests.post(
        settings.GOOGLE_VERIFY_RECAPTCHA_URL,
        data={
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': request.POST.get('g-recaptcha-response'),
        },
        verify=True
    ).json().get("success", False)
