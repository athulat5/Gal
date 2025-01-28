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
]



