from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from shop.models import Category, Product, ImageProduct, Order, Cart
from shop.serializers import *
from shop.permissions import *


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProductUserViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = ProductListSerializer
    detail_serializer_class = ProductDetailSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        category = self.request.GET.get('category')

        if category is not None:
            queryset = queryset.filter(category=Category.objects.get(name=category))

        return queryset


class CategoryUserViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.all()


class CartUserViewSet(RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAdminAuthenticated]

    def get(self, request, *args, **kwargs):
        return Cart.Objects.get(user=request.user)


# admin views


class ProductAdminViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProductListSerializer
    detail_serializer_class = ProductDetailSerializer
    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        category = self.request.GET.get('category')
        if category is not None:
            return Product.objects.filter(category=Category.objects.get(name=category))
        return Product.objects.all()


class CategoryAdminViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        return Category.objects.all()
