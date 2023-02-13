from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=False, default='')

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Называние')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='product_image', verbose_name='Изображение')
    price = models.IntegerField(verbose_name='Цена')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)


# class Order(models.Model):
#     first_name = models.CharField(max_length=200, verbose_name='Имя')
#     last_name = models.CharField(max_length=200, verbose_name='Фамилия')
#     address = models.TextField(verbose_name='Адрес')
#     productes = models.ForeignKey(Product, on_delete=models.CASCADE)
#     amount = models.CharField(max_length=10, verbose_name='Колличество')
#     total_price = models.CharField(max_length=100, verbose_name='Сумма')



