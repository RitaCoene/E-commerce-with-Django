from django.db import models
# from django.contrib.postgres.fields import ArrayField

# Create your models here.




class Product(models.Model):
    img = models.ImageField()
    categorie = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.CharField(max_length=10000, default='This product has no description')
    rebate = models.IntegerField()
    no_of_likes = models.IntegerField(default=0)



    def __str__(self):
        return self.title



class Favorite(models.Model):
    product_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)




