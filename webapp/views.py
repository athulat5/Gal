
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages,auth
from django.contrib.auth.forms import User
from .models import Customer,Seller,Product, Cart
from django.utils.html import format_html
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from django.shortcuts import get_object_or_404

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

def customer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if Customer.objects.filter(customer=request.user).exists():
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You are not authorized to access this page.")
        return redirect('login')  # Redirect to login if not authenticated
    return wrapper

def seller_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if Seller.objects.filter(seller=request.user).exists():
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You are not authorized to access this page.")
        return redirect('sellerlogin')  # Redirect to login if not authenticated
    return wrapper




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

@login_required
@customer_required
def user(request):
    products = Product.objects.all()
    return render(request, 'user.html', {'products': products}) 
   
@login_required
@seller_required
def sellerhome(request):
    products = Product.objects.all()
    return render(request, 'sellerhome.html', {'products': products})                                                                                                                                                                                                                                                                                                                         

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('user_login') 
 
def seller_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('seller_login')  

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('sellerhome')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})



def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first() 
    products = cart.products.all() if cart else []  
    return render(request, 'cart.html', {'products': products})


def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Check if the product is already in the cart
        if product in cart.products.all():
            return JsonResponse({"message": f"{product.name} is already in your cart."})
        
        # Add product to cart
        cart.products.add(product)
        return JsonResponse({"message": f"{product.name} added to cart!"})
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)

@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart.products.remove(product)

    return redirect('cart_view')

@login_required
def remove_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('sellerhome')

def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('sellerhome') 
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})