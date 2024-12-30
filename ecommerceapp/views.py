from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Avg
from datetime import datetime, timedelta

# Create your views here.

@login_required
def home(request):
    categories=Category.objects.all()
    return render(request,'home.html',{'categories':categories})

def loginview(request):
    uname=request.POST['username']
    pwd=request.POST['password']
    user=authenticate(username=uname,password=pwd)
    if user is not None:
        login(request,user)
        return redirect('home')
    return render(request,'login.html',{'msg':'Invalid user credentials !'})

def logoutview(request):
    logout(request)
    return redirect('login')

def signupview(request):
    try:
        form=UserCreationForm(request.POST)
        if request.method=='POST':
            if form.is_valid():
                form.save()
                return redirect('login')
            return render(request,'signup.html',{'msg':'Invalid User Login!'})
        else:
            form=UserCreationForm()
            return render(request,'signup.html',{'form':form})
    except Exception as e:
        print(e)
        form=UserCreationForm()
        return render(request,'signup.html',{'form':form})

def products_view(request):
    product=Product.objects.all()
    return render(request,'products_view.html',{'product':product})

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    categories=Category.objects.all()
    products = Product.objects.filter(product_category=category,product_stock__gt=0)
    wishlist_items = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    if request.method == 'POST':
        name = request.POST['brand']
        products = products.filter(Q(product_brand__icontains=name) | Q(product_name__icontains=name))

    return render(request, 'category_wise_products.html', {
        'category': category,
        'products': products,
        'wishlist_items': wishlist_items,
        'categories':categories,    
    })

def individual_product(request,product_id):
    product=Product.objects.get(id=product_id)
    wishlist_items = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    review=Review.objects.filter(product=product)
    avg_rating = review.aggregate(Avg('rating'))['rating__avg'] or 0
    avg_rating=round(avg_rating,1)
    category=product.product_category
    brand=product.product_brand
    current_date=datetime.now().date()
    delivery_date=current_date+timedelta(days=5)
    related_products = Product.objects.filter(
        product_category=category,
        product_brand=brand
    ).exclude(id=product_id)
    return render(request,'individual_product.html',{'item':product,'wishlist_items': wishlist_items,'review':review,'avg_rating':avg_rating,'related_products': related_products,'delivery_date':delivery_date})

def order(request,product_id):
    product=get_object_or_404(Product,id=product_id) 
    order_date=datetime.now().date()
    delivery_date=order_date+timedelta(days=5)
    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            order=form.save(commit=False)
            order.product=product
            order.user=request.user
            order.save()
            product.product_stock-=1
            product.save()
            payment_method=form.cleaned_data.get('payment_method')
            if payment_method=='cash':
                return redirect('order_placed',product_id=product.id)
            elif payment_method=='card':
                # return redirect('card_details',product_id=product.id)
                return render(request,'card_details.html',{'product':product})
    else:
        form=OrderForm()
    return render(request,'order.html',{'form':form,'product':product,'delivery_date':delivery_date})

def add_to_cart(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    cart,created=Cart.objects.get_or_create(user=request.user)
    cart_item,created=CartItem.objects.get_or_create(product=product,cart=cart)
    if not created:
        cart_item.quantity+=1
        cart_item.save()
        messages.success(request, f"{product.product_name} added to cart successfully!")
    else:
        cart_item.quantity=1
        cart_item.save()
        messages.success(request, f"{product.product_name} added to cart successfully!")
    return redirect('cart_view')

def cart_view(request):
    cart=Cart.objects.get(user=request.user)
    items=cart.items.all()
    total_price=0
    for item in items:
        total_price=total_price+item.get_total_price()
    return render(request, 'cart_view.html', {'cart': cart, 'items': items, 'total_price': total_price})

def add_to_wishlist(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    wishlist=Wishlist.objects.get_or_create(user=request.user,product=product)
    return redirect('wishlist')

def wishlist(request):
    wishlist=Wishlist.objects.filter(user=request.user)
    wishlist_items = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    # items=wishlist.items.all()
    return render(request,'wishlist.html',{'items':wishlist,'wishlist_items': wishlist_items})

def order_placed(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    return render(request,'order_placed.html',{'product':product})

def card_details(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    return redirect('order_placed',product_id=product.id)

def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

    if cart_item:
        cart_item.delete()
        messages.success(request, 'Item removed from cart successfully.')
    else:
        messages.error(request, 'Item not found in your cart.')

    return redirect('cart_view')


def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        wishlist_item.delete()
        messages.success(request, f"{product.product_name} was removed from your wishlist.")
    else:
        messages.success(request, f"{product.product_name} was added to your wishlist.")
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('category_products', slug=product.product_category.slug)
    
def completed_orders(request):
    completed_products = Order.objects.filter(status='delivered', user=request.user)

    if request.method == 'POST':
        # Check if the form is submitted for a specific product
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            # Create or update review
            review = review_form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('completed_orders')  # Redirect after form submission to avoid resubmission

    else:
        review_form = ReviewForm()
    return render(request, 'completed_orders.html', {'completed_products': completed_products, 'review_form': review_form})


def yettodeliver(request):
    yettodeliver = Order.objects.filter(Q(status='pending') | Q(status='shipped'))
    return render(request, 'yettodeliver.html', {'yettodeliver': yettodeliver})
