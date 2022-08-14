from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

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


class CartUserViewSet(ModelViewSet):
    serializer_class = CartListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def gcoc(self, request): #get cart or create
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user, ordered=False)

        if created:
            return Response(CartSerializer(cart).data, status=201)
        return Response(CartSerializer(cart).data, status=200)

    @action(detail=False, methods=['PUT'])
    def ordered(self, request):
        user = request.user
        cart = Cart.objects.get(user=user, ordered=False)
        cart.make_ordered()

        return Response(status=200)


class OrderUserViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user, ordered=False)
        product_id = request.POST['product']
        product = Product.objects.get(id=product_id)
        quantity = request.POST['quantity']
        new_order = Order.objects.create(user=user, cart=cart, product=product, quantity=quantity)

        serializer = OrderSerializer(new_order)
        return Response(serializer.data)



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


class CartAdminViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CartListSerializer
    detail_serializer_class = CategoryDetailSerializer
    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        return Cart.objects.all()


class UserAdminViewset(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        user_model = get_user_model()
        return user_model.objects.all()
