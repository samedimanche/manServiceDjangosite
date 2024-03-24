from django.db import models
from django.contrib.auth.models import User


class CategoryProduct(models.Model):
    category = models.CharField('Название категории', max_length=200)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категория Товара'
        verbose_name_plural = 'Категории Товаров'


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField('Имя',max_length=200, null=True)
    email = models.CharField('Email',max_length=200, null=True)
    phone = models.CharField('Телефон',max_length=200, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Product(models.Model):
    name = models.CharField('Название', max_length=200)
    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, null=True, blank=True, related_name='products', verbose_name='Категория товара')
    price = models.DecimalField('Цена', max_digits=7, decimal_places=2)
    image = models.ImageField('Фото товара', null=True, blank=True)
    AVAILABILITY_CHOICES = (('available', 'В наличии'), ('not_available', 'Нет в наличии'))
    product_availability = models.CharField('Наличие', max_length=20, choices=AVAILABILITY_CHOICES, null=True, blank=True, default='available')
    STATUS = (('new', 'Новый'), ('not_new', 'Б/у'))
    status = models.CharField('Статус', max_length=20, choices=STATUS, null=True, blank=True, default='new')
    ORIGINALITY = (('original', 'Оригинал'), ('not_original', 'Не оригинал'))
    originality = models.CharField('Оригинальность', max_length=25, choices=ORIGINALITY, null=True, blank=True, default='original')
    producer = models.CharField('Производитель', max_length=250, null=True, blank=True, default='Sinotruck')
    part_number = models.CharField('Номер запчасти', max_length=250)
    fit = models.CharField('Подходит для моделей', max_length=250, null=True, blank=True, default='Howo T5G, Sitrak C7H')
    description = models.TextField('Описание', null=True, blank=True, default='Собственный склад запасных частей в Благовещенске. '
                                                                              'У нас имеется в наличии множество позиций запчастей для грузовых автомобилей. '
                                                                              'Работаем по договору, безналичная и наличная оплата, НДС. ')
    digital = models.BooleanField(default=False, null=True, blank=False)


    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.CharField('Регион', max_length=200, null=True)
    state = models.CharField('Город', max_length=200, null=True)
    address = models.CharField('Адрес', max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Адрес Клиента'
        verbose_name_plural = 'Адреса Клиентов'


