
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages,auth
from django.contrib.auth.forms import User
from .models import Customer,Seller
from django.utils.html import format_html

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request,user)
            try:
                if Customer.objects.filter(customer=user).exists():
                     return redirect('user')
                else:
                    error_message = "Invalid credentials. Please try again."
                    return render(request, 'login.html', {'error': error_message})
                
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('/')
 
        else:
            error_message = "Invalid credentials. Please try again."
            return render(request, 'login.html', {'error': error_message})

    return render(request, 'login.html')

def seller_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request,user)
            try:
                if Seller.objects.filter(seller=user).exists():
                     return redirect('sellerhome')  
                else:
                    error_message = "Invalid credentials. Please try again."
                    return render(request, 'sellerlog.html', {'error': error_message})

                
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('/')
 
        else:
            error_message = "Invalid credentials. Please try again."
            return render(request, 'sellerlog.html', {'error': error_message})

    return render(request, 'sellerlog.html')

def signup(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('ConfirmPassword')

        # Validate form inputs
        if not username or not email or not password or not confirm_password:
            messages.error(request, 'All fields are required.')

        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")

        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")

        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")

        else:
            # Create and save the user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            customer = Customer(customer=user)
            customer.save()
            messages.success(request, "Account created successfully.")
            return redirect('user_login') 

        # If there are validation errors, render the form again with messages
        return render(request, 'signup.html', {'username': username, 'email': email})

    return render(request, 'signup.html')


def user(request):
    return render(request, 'user.html')  


def seller_signup(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('ConfirmPassword')

        # Validate form inputs
        if not username or not email or not password or not confirm_password:
            messages.error(request, 'All fields are required.')

        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")

        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")

        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")

        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            seller = Seller(seller=user)
            seller.save()
            return redirect('user_login') 

        # If there are validation errors, render the form again with messages
        return render(request,'sellerreg.html', {'username': username, 'email': email})

    return render(request, 'sellerreg.html')

def sellerhome(request):
   
  return render(request, 'sellerhome.html')                                                                                                                                                                                                                                                                                                                         


 

