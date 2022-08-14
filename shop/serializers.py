from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError, ListField, FileField
from django.contrib.auth import get_user_model

from ecommerce_api.settings import AUTH_USER_MODEL
from .models import Product, ImageProduct, Category, Order, Cart




class CategoryListSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class CategoryDetailSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'date_created', 'date_updated']


class ImageSerializer(ModelSerializer):

    class Meta:
        model = ImageProduct
        fields = ['upload']


class ProductListSerializer(ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    uploaded_images = ListField(
        child=FileField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        allow_empty=False,
        max_length=4
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'images', 'uploaded_images', 'category']

    def create(self, validated_data):
        uploaded_data = validated_data.pop('uploaded_images')
        new_product = Product.objects.create(**validated_data)
        for uploaded_item in uploaded_data:
            new_product_image = ImageProduct.objects.create(product=new_product, upload=uploaded_item)
        return new_product




class ProductDetailSerializer(ModelSerializer):

    category = CategoryDetailSerializer(many=False)
    images = ImageSerializer(many=True)
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'stock', 'images', 'date_created', 'date_updated']


class OrderSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class CartListSerializer(ModelSerializer):
    orders = OrderSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['user', 'orders', 'ordered']


class CartDetailSerializer(ModelSerializer):
    orders = OrderSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'


class UserSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        exclude = ('password', )
