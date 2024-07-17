from django.contrib import admin
from django.urls import path
from gamestopapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.index),
    path('products',views.createProduct),
    path('products/view',views.readProduct),
    path('products/edit/<rid>',views.updateProduct),
    path('products/delete/<rid>',views.deleteProduct),
    path('products/details/<rid>',views.productDetails),

    path('register',views.userRegister),
    path('login',views.userLogin),
    path('logout',views.userLogout),
    path('users/view',views.readUser),
    path('users/edit/<rid>',views.updateUser),
    path('add_to_cart/<rid>',views.add_to_cart),
    path('cart',views.cart),
    path('remove_cart/<rid>',views.removeCart),
    path('cart/update/<cid>/<rid>',views.updateCart),   # cid = quantity and rid = cart Id

    path('add_to_order',views.add_to_order),

    path('orders',views.show_orders),

    path('add_review/<rid>',views.add_review),

    path('forgot_password',views.forgot_password),

    path('verify_otp',views.verify_otp),

    path('change_password',views.change_password)
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

