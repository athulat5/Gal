# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [


    path('', views.user_login, name='user_login'),
    path('signup/', views.signup, name='signup'),
    path('user/', views.user, name='user'),
    path('seller_signup/',views.seller_signup,name='seller_signup'),
    path('seller_login/',views.seller_login,name='seller_login'),
    path('seller/', views.seller, name='seller'),  
    path('sellerhome/',views.sellerhome,name='sellerhome')
    
   
]



