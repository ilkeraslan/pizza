import requests
import json

from decimal import *

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .forms import CustomLoginForm, SignupForm

from .models import Cart, Entry, Pizza, Size, Topping


class IndexView(generic.ListView):

    # Use existing template
    template_name = 'orders/index.html'

    # Pass context object
    context_object_name = 'menu_list'

    def get_queryset(self):

        # Number of visits to this view
        # Get the value of visit_number session key, set to 0 if it has not been set
        self.visit_number = self.request.session.get('visit_number', 0)
        self.request.session['visit_number'] = self.visit_number + 1
        return Pizza.objects.all()

    # Override get_context_data() method to addd extra content
    def get_context_data(self, **kwargs):
        # Call the base implementation
        context = super().get_context_data(**kwargs)

        # Add visit numbers
        context['visit_number'] = self.visit_number

        # Return context
        return context


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

        if form.is_valid():

            # Check the recaptch field
            if not is_recaptcha_valid(request):
                messages.error(request, "Invalid recaptcha.")
                return render(request, 'registration/login.html', {'form': CustomLoginForm()})

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # Redirect to index
                messages.success(request, "Logged in.")
                return HttpResponseRedirect(reverse('orders:index'))
            else:
                messages.error(request, "Invalid credentials.")

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


def logout_view(request):
    logout(request)

    # Redirect to login with a message
    messages.success(request, "Successfully logged out.")
    return HttpResponseRedirect(reverse('orders:index'))


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


def view_cart(request):

    # If user has not logged-in, redirect to login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('orders:login'))

    # Get the cart object for the corresponding user
    user_cart, created = Cart.objects.get_or_create(user=request.user)

    # Get a queryset of entries that correspond to 'user_cart'
    list_of_entries = Entry.objects.filter(cart=user_cart)

    context = {
        'cart': list_of_entries,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }

    return render(request, 'orders/cart.html', context)


def add_to_cart(request):

    # If user has not logged-in, redirect to login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('orders:login'))

    # Get or create the cart for the current user
    user_cart, created = Cart.objects.get_or_create(user=request.user)

    # Get the pizza ID from the request
    pizzaId = request.POST['pizzaId']

    # Get the quantity from the request
    pizza_quantity = request.POST['pizza_quantity']

    # Cast it to Decimal to be able to multiply it with an int
    pizza_quantity = Decimal(pizza_quantity)

    # Get the pizza from the database that has the corresponding ID
    pizza_to_add = Pizza.objects.get(id=pizzaId)

    # Create new entry which will update the cart
    Entry.objects.create(cart=user_cart, pizza=pizza_to_add, quantity=pizza_quantity, topping=None)

    # Give success feedback
    messages.success(request, "Added to cart.")

    return HttpResponseRedirect(reverse('orders:details', args=(pizzaId,)))


def add_topping(request):

    # If request is not a POST request, return index
    if request.method == 'POST':

        # Get the cart for the current user
        user_cart = Cart.objects.get(user=request.user)

        # Get the pizza ID from the request
        pizzaId = request.POST.get('pizzaId')

        # Get the data from the POST request
        topping_selected = request.POST.get('topping_selected')

        # Topping quantity is 1 by default
        topping_quantity = 1

        # Get the topping from the database that has the corresponding ID
        topping_to_add = Topping.objects.get(id=topping_selected)

        # Create new entry which will update the cart
        Entry.objects.create(cart=user_cart, topping=topping_to_add, quantity=topping_quantity, pizza=None)

        # Give success feedback
        messages.success(request, "Added the topping.")

        return HttpResponseRedirect(reverse('orders:details', args=(pizzaId,)))

    return HttpResponseRedirect(reverse('orders:index'))


def clear_cart(request):
    if request.method == 'POST':

        # Get the user cart
        user_cart = Cart.objects.filter(user=request.user)

        # Delete all entries of user cart
        cart_entries = Entry.objects.filter(cart__in=user_cart).delete()

        # Print how many items were deleted
        messages.success(request, "Deleted " +str(cart_entries[0]) + " items.")

    return HttpResponseRedirect(reverse('orders:cart'))


def checkout(request):

    # If user has not logged-in, redirect to login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('orders:login'))

    # If user came via a POST request
    if request.method == 'POST':

        context = {
            'stripe_public_key': request.POST.get('stripe_public_key')
        }
        return render(request, 'orders/checkout.html', context)

    # Else return cart view
    messages.error(request, "You should control your cart before checkout.")
    return HttpResponseRedirect(reverse('orders:cart'))


def charge(request):

    # If user has not logged-in, redirect to login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('orders:login'))

    # If user came via a POST request
    if request.method == 'POST':
        return render(request, 'orders/thankyou.html')

    # Else return cart view
    messages.error(request, "You are not authorized to pay.")
    return HttpResponseRedirect(reverse('orders:cart'))
