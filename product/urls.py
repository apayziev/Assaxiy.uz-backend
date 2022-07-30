from django.urls import path
from product.views import *

urlpatterns = [
    path('product-list/', ProductList.as_view()),
    path('product-detail/<int:pk>/', ProductDetail.as_view()),
    path('category-list/', CategoryList.as_view()),
    path('card-list/', CardList.as_view()),
    path('product-image-list/', ProductImageList.as_view()),
    path('product-option-list/', ProductOptionList.as_view()),
    path('product-option-value-list/', ProductOptionValueList.as_view()),
    path('order-product/', OrderProductList.as_view()),
    path('comment-list/', CommentList.as_view()),
]