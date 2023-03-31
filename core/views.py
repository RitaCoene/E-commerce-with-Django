from django.shortcuts import render, redirect
from .models import Product, Favorite
from django.contrib import messages
from itertools import chain
from django.contrib.auth.decorators import login_required
import random   
from django.contrib import messages
from django.contrib.auth.models import User, auth



# Create your views here.
@login_required(login_url='register')
def index(request):
    products = Product.objects.all()
    user = User.objects.filter(username=request.user.username)
    return render(request, 'index.html', {'products':products})

@login_required(login_url='register')
def product(request, pk):
    product = Product.objects.get(id=pk)
    productsP = Product.objects.all()
    products = []

    for productP in productsP :
        if productP != product and len(products) < 3:
            products.append(productP)

    return render(request, 'product.html', {'product':product, 'products':products})




@login_required(login_url='register')
def favorite(request, pk):
    username = request.user.username
    product_id = pk 

    product = Product.objects.get(id=product_id)

    favorite_filter = Favorite.objects.filter(product_id=product_id, username=username).first()





    if favorite_filter == None:
        new_favorite = Favorite.objects.create(product_id=product_id, username=username)
        new_favorite.save()
        product.no_of_likes = product.no_of_likes+1
        product.save()


        return redirect('/')

    else:
        favorite_filter.delete()
        product.no_of_likes = product.no_of_likes-1
        product.save()

        return redirect('/')


@login_required(login_url='register')
def cart(request):
    username = User.objects.get(username=request.user.username)
    productsT = Product.objects.all()
    favorites = Favorite.objects.all()
    products = []

    for favorite in favorites:
        if favorite.username == username.username:
            product_id = favorite.product_id
            product = Product.objects.get(id=product_id)
            products.append(product)
        





    return render(request, 'cart.html', {'username':username, 'products':products, 'favorites':favorites})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']


        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('register')
            

    else:
        return render(request, 'register.html')

def login(request):

    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password']


        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('login') 
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('login') 
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                return redirect('register')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('login')
    
    else: 
        return render(request, 'login.html')

@login_required(login_url='register')
def logout(request):
    auth.logout(request)
    return redirect('/')