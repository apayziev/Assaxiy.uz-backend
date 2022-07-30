from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
from common.models import User
from helpers.models import BaseModel


class District(BaseModel):
    name = models.CharField(max_length=255, verbose_name="District Name")

    def __str__(self):
        return self.name


class Region(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Region Name")
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name="regions"
    )

class Category(BaseModel):
    """Category model"""
    title = models.CharField(max_length=256)
    slug = models.CharField(max_length=256)
    icon = models.FileField(upload_to="category/", null=True, blank=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)


class Product(BaseModel):
    title = models.CharField(max_length=256)
    slug = models.CharField(max_length=256)
    content = RichTextUploadingField()
    image = models.ImageField(upload_to="product_image", editable=False, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    in_stock = models.IntegerField(default=0)

    price = models.DecimalField(
        max_digits=19, decimal_places=2, verbose_name="Sotilish narxi"
    )
    price_discount = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Chegirmadagi narxi(ustiga chizilgan)",
    )

    rate = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    saveds = models.ManyToManyField(User, related_name="saveds", blank=True)

    options = models.ManyToManyField(
        "ProductOptionValue", blank=True, null=True, related_name="products"
    )

    def set_image(self):
        main_image = ProductImage.objects.filter(product=self, is_main=True).first()
        self.image = main_image
        self.save()


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_image")
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return self.product.title

class ProductOption(BaseModel):
    title = models.CharField(max_length=256)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, related_name="options"
    )
    is_filter = models.BooleanField(default=False)


class ProductOptionValue(BaseModel):
    title = models.CharField(max_length=256)
    option = models.ForeignKey(
        ProductOption, on_delete=models.CASCADE, null=True, related_name="values"
    )


class Card(BaseModel):
    product_price = models.DecimalField(
        max_digits=19, decimal_places=2, verbose_name="Product price"
    )
    count = models.IntegerField(default=1)

    @property
    def total_price(self):
        return self.product_price * self.count


class Order(BaseModel):
    full_name = models.CharField(max_length=256)
    phone = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name="orders"
    )
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="orders")
    job_address = models.CharField(max_length=256, null=True, blank=True)
    extra = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Card, related_name="orders")
    total_price = models.DecimalField(
        max_digits=19, decimal_places=2, verbose_name="Total price"
    )
    payment_type = models.CharField(
        max_length=256,
        choices=(
            ("cash", "By cash"),
            ("card", "By card"),
        ),
    )
    payment_rules = models.CharField(
        max_length=256,
        choices=(
            ("agree", "Agree"),
            ("disagree", "Disagree"),
        ),
    )
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.total_price}"


class OrderProduct(BaseModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_products"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_products"
    )
    count = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=19, decimal_places=2, verbose_name="Price")
    

    def __str__(self):
        return f"{self.order} - {self.product}"


class Comment(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)
    content = models.TextField()
