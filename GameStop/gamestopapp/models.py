from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):

    type = (('Adventure','Adventure'),('RPG','RPG'),('Action','Action'),('Racing','Racing'),('Puzzle','Puzzle'))

    name = models.CharField(max_length = 200)
    description = models.CharField(max_length = 200)
    manufacturer = models.CharField(max_length = 200)
    price = models.FloatField()
    category = models.CharField(max_length = 200,choices = type)
    isAvailable = models.BooleanField(default = True)
    image = models.FileField()
    # here in image put default value as 1 in terminal that is through console 2nd opt is different


    def __str__(self):
        return self.name

class Cart(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)
    price = models.FloatField()

    def __str__(self):
        return self.user.username


class Review(models.Model): 

    rate = ((1,1),(2,2),(3,3),(4,4),(5,5))

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    rating = models.IntegerField(choices = rate)
    image = models.FileField(upload_to = 'reviewImages')
    review = models.CharField(max_length = 200)

    def __str__(self):
        return self.product.name

class Orders(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()

    

