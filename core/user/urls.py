from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='user_home'),
    path('register/', views.register_view, name='user_register'),
    path('login/', views.login_view, name='user_login'),
    path('logout/', views.logout_view, name='user_logout'),

    path('profile/', views.profile, name='user_profile'),
    path('payment/', views.payment, name='user_payment'),

    path('businesses/', views.business_list, name='business_list'),
    path('business/<int:business_id>/', views.business_menu, name='business_menu'),
 
    
]
