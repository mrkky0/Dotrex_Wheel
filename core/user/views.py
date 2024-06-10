from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from owner.models import Business, Product
# Create your views here.

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Şifreler eşleşmiyor.")
            return render(request, 'user/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu kullanıcı adı zaten alınmış.")
            return render(request, 'user/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Bu email zaten kullanılıyor.")
            return render(request, 'user/register.html')

        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            login(request, user)
            # Business.objects.get_or_create(user=user, name=username)

         
        except:
            messages.error(request, "Hata")
            return render(request, 'user/register.html')
            
        return redirect('user_home')

    return render(request, 'user/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'user_home')
            return redirect(next_url)
        else:
            messages.error(request, "Geçersiz kullanıcı adı veya şifre.")
    
    return render(request, 'user/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('user_home')  




def business_list(request):
    businesses = Business.objects.all()
    return render(request, 'user/business_list.html', {'businesses': businesses})

def business_menu(request, business_id):
    business = get_object_or_404(Business, id=business_id)
    products = Product.objects.filter(business=business)
    return render(request, 'user/business_menu.html', {'business': business, 'products': products})



def profile(request):
    user = request.user
    return render(request, 'user/profile.html',{'userName':user.username})

def payment(request):
    return render(request, 'user/payment.html')

def home(request):
    return render(request, 'user/home.html')


