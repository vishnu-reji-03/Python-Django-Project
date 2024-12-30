from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category_title=models.CharField(max_length=100)
    category_image=models.ImageField(upload_to='category_images')
    slug=models.SlugField(unique=True)
    category_description=models.CharField(max_length=200)
    def __str__(self):
        return self.category_title


class Product(models.Model):
    product_name=models.CharField(max_length=100)
    product_category=models.ForeignKey(Category,on_delete=models.CASCADE)
    product_image=models.ImageField(upload_to='product_images')
    product_brand=models.CharField(max_length=100)
    product_original_price=models.IntegerField()
    product_selling_price=models.IntegerField()
    small_description=models.CharField(max_length=400)
    large_description=models.CharField(max_length=800)
    product_stock=models.IntegerField()
    product_available=models.BooleanField(default=True)
    def __str__(self):
        return f"{self.product_name,self.id}"

class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=100)
    phone=models.IntegerField()
    email=models.EmailField()
    quantity=models.PositiveIntegerField(default=1)
    order_date=models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=10,
        choices=[('cash', 'Cash on Delivery'), ('card', 'Credit/Debit Card')],
        default='cash'
    )
    status=models.CharField(max_length=50,choices=[('pending','pending'),('delivered','delivered'),('shipped','shipped')],default='pending')
    def __str__(self):
        return f"Order{self.id}by{self.user.username}"
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.product_selling_price*self.quantity
    def get_total_cart_price(self):
        return sum(item.get_total_price() for item in self.items.all())
    
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    added_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product_name,self.id}added by{self.user.username}"
    
class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    rating=models.IntegerField(default=0)   
    comment=models.TextField(blank=True,null=True)
    review_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product_name}review by{self.user.username}"