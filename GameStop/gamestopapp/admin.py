from django.contrib import admin
from gamestopapp.models import Product,Cart,Orders,Review
# Register your models here.

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Orders)
admin.site.register(Review)
