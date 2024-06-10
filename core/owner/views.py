# accounts/views.py

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from datetime import timedelta

from django.contrib.auth.models import User
from .models import Coupon,Product,Business
from .forms import ProductForm


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Şifreler eşleşmiyor.")
            return render(request, 'owner/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu kullanıcı adı zaten alınmış.")
            return render(request, 'owner/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Bu email zaten kullanılıyor.")
            return render(request, 'owner/register.html')

        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            login(request, user)
            Business.objects.get_or_create(user=user, name=username)

         
        except:
            messages.error(request, "Hata")
            return render(request, 'owner/register.html')
            
        return redirect('owner_home')

    return render(request, 'owner/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'owner_home')
            return redirect(next_url)
        else:
            messages.error(request, "Geçersiz kullanıcı adı veya şifre.")
    
    return render(request, 'owner/login.html')

def home(request):
    return render(request,'owner/home.html',{})



@login_required
def payment(request):
    user = request.user
    return render(request,'owner/payment.html',{'users':user.username})

 
def coupon_list(request):
    now = timezone.now()
    coupons = Coupon.objects.filter(valid_from__lte=now, valid_to__gte=now, active=True)
    return render(request, 'owner/coupon_list.html', {'coupons': coupons})

def create_coupon(request):
    if request.method == "POST":
        discount = request.POST.get('discount', 10.00)
        valid_from = timezone.now()
        valid_to = valid_from + timedelta(seconds=25)
        coupon = Coupon.objects.create(discount=discount, valid_from=valid_from, valid_to=valid_to)
        return redirect('coupon_list')
    return render(request, 'owner/create_coupon.html')


@login_required
def profile(request):
    business = get_object_or_404(Business, user=request.user)
    return render(request, 'owner/profile.html', {'business': business})

@login_required
def create_product(request):
    business = get_object_or_404(Business, user=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.business = business
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'owner/create_product.html', {'form': form})

@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk, business__user=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'owner/update_product.html', {'form': form})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, business__user=request.user)
    if request.method == "POST":
        product.delete()
        return redirect('product_list')
    return render(request, 'owner/delete_product.html', {'product': product})

@login_required
def product_list(request):
    business = get_object_or_404(Business, user=request.user)
    products = Product.objects.filter(business=business)
    return render(request, 'owner/product_list.html', {'products': products})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('owner_home')  