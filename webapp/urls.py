# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('signup/', views.signup, name='signup'),
    path('user/', views.user, name='user'),
    path('seller_signup/',views.seller_signup,name='seller_signup'),
    path('seller/', views.seller_login, name='seller_login'),  
    path('sellerhome/',views.sellerhome,name='sellerhome'),
    path('logout/', views.user_logout, name='user_logout'),
    path('seller_logout/', views.seller_logout, name='seller_logout'),
    path('add-product/', views.add_product, name='add_product'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove_product/<int:product_id>/', views.remove_product, name='remove_product'),
    path('edit-product/<int:id>/', views.edit_product, name='edit_product'),
    
]



