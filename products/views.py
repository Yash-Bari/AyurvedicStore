from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Product
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout_view(request):
    orders = Order.objects.filter(user=request.user, status='Pending')
    total_price = sum(order.product.price for order in orders)
    return render(request, 'checkout.html', {'orders': orders, 'total_price': total_price})

@login_required
def payment_process_view(request):
    orders = Order.objects.filter(user=request.user, status='Pending')
    total_price = sum(order.product.price for order in orders)

    intent = stripe.PaymentIntent.create(
        amount=int(total_price * 100),  # Amount in cents
        currency='usd',
        metadata={'user_id': request.user.id}
    )

    return render(request, 'payment_process.html', {'client_secret': intent.client_secret})


@login_required
def cart_add_view(request, pk):
    product = Product.objects.get(pk=pk)
    order = Order(user=request.user, product=product)
    order.save()
    return redirect('cart')

@login_required
def cart_view(request):
    orders = Order.objects.filter(user=request.user, status='Pending')
    total_price = sum(order.product.price for order in orders)
    return render(request, 'cart.html', {'orders': orders, 'total_price': total_price})

@login_required
def order_confirm_view(request):
    orders = Order.objects.filter(user=request.user, status='Pending')
    for order in orders:
        order.status = 'Confirmed'
        order.save()
    return redirect('cart')


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product-list')
        return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    form = UserProfileForm(instance=user_profile)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    return render(request, 'profile.html', {'form': form})


class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'product_list.html', {'products': products})

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'product_detail.html', {'product': product})

class RegistrationView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('product-list')
        return render(request, 'register.html', {'form': form})
