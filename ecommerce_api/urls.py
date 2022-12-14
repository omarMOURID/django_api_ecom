"""ecommerce_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from shop.views import *

#ici nous créons notre routeur
router = routers.SimpleRouter()
# puis lui déclarons une url basée sur le mot clé 'category' et notre view
# afin que l'yrl générée soit celle que nous souhaitons '/api/category/'

router.register('admin/category', CategoryAdminViewset, basename='admin-category')
router.register('admin/product', ProductAdminViewset, basename='admin-product')
router.register('admin/cart', CategoryAdminViewset, basename='admin-cart')
router.register('admin/user', UserAdminViewset, basename='admin-user')
router.register('category', CategoryUserViewset, basename='category')
router.register('product', ProductUserViewset, basename='product')
router.register('user/order', OrderUserViewSet, basename='order')
router.register('user/cart', CartUserViewSet, basename='cart')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)