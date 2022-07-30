from rest_framework.permissions import IsAuthenticated
from django.views.decorators.vary import vary_on_headers, vary_on_cookie
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from helpers.pagination import CustomPagination

from product.models import Product, ProductOptionValue,ProductOption, Card, ProductImage, Category, Comment
from product.serializers import *

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CardList(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class ProductImageList(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class ProductOptionList(generics.ListCreateAPIView):
    queryset = ProductOption.objects.all()
    serializer_class = ProductOptionSerializer

class ProductOptionValueList(generics.ListCreateAPIView):
    queryset = ProductOptionValue.objects.all()
    serializer_class = ProductOptionValueSerializer

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all().select_related('category').prefetch_related('images', 'options',)
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    
    # Cache page for the requested urls
    @method_decorator(cache_page(60*60*2))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class OrderProductList(generics.ListCreateAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer


class CommentList(generics.ListAPIView):
    queryset = Comment.objects.
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    
    




