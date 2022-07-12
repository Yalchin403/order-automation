from unittest.util import _MAX_LENGTH
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


class Employee(models.Model):
    name = models.CharField(max_length=55)
    surname = models.CharField(max_length=55)
    profession = models.CharField(max_length=55)
    description = models.TextField()
    email = models.EmailField(max_length=55)
    image = models.ImageField(upload_to='employees/%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"


class Category(models.Model):
    name = models.CharField(max_length=55, unique=True)
    slug = models.SlugField(null=True, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/")

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("home:products_by_category", args=[self.slug])
    
    class Meta:
        verbose_name_plural = "Categories"


class ProductImage(models.Model):
    image = models.ImageField(upload_to="products/%Y/%m/%d/")

    def __str__(self) -> str:
        return self.image.name

class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(null=True, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.FloatField()
    images = models.ManyToManyField('ProductImage', related_name="products")
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("home:product_detail", args=[self.category.slug, self.slug])


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return "{self.cart_id} - {self.date_added}"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.product