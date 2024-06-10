from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='owner_register'),
    path('login/', views.login_view, name='owner_login'),
    path('logout/', views.logout_view, name='owner_logout'),
    path('', views.home, name='owner_home'),
    path('profile/', views.profile, name='owner_profile'),
    
    path('products/', views.product_list, name='product_list'),
    path('create_product/', views.create_product, name='create_product'),
    path('update_product/<int:pk>/', views.update_product, name='update_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),

    path('coupons/', views.coupon_list, name='coupon_list'),
    path('create_coupon/', views.create_coupon, name='create_coupon'),
    path('payment/', views.payment, name='owner_payment'),
    
]
