from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Называние')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='product_image', verbose_name='Изображение')
    price = models.IntegerField(verbose_name='Цена')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)