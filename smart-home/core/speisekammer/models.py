from django.utils import timezone
from django.db import models

# Create your models here.
from django.db.models import Sum
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    stock_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['name']

    def stock_io(self, io, barcode=None):
        if barcode is None:
            ProductInstance.objects.get_or_create(product=self, barcode__exact='')[0].stock_io(io)
        else:
            ProductInstance.objects.get_or_create(product=self, barcode=barcode)[0].stock_io(io)

    def item_count(self):
        return self.instances.aggregate(item_count=Sum('item_count'))['item_count']

    def count_difference(self):
        return self.stock_count - self.item_count() if self.stock_count > self.item_count() else 0

    def get_absolute_url(self):
        return reverse('speisekammer:product_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class ProductInstance(models.Model):
    product = models.ForeignKey(Product, related_name='instances', on_delete=models.CASCADE)
    barcode = models.CharField(max_length=100, blank=True)
    item_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'barcode')

    def stock_io(self, io):
        self.item_count += io
        if self.item_count < 0:
            self.item_count = 0
        self.save()

    def get_absolute_url(self):
        return reverse('speisekammer:instance_detail', kwargs={'pk': self.product.pk, 'barcode': self.barcode})

    def __str__(self):
        return self.barcode


class ShoppingList(models.Model):
    name = models.CharField(max_length=100, blank=True)
    creation = models.DateTimeField()
    completion = models.DateTimeField(blank=True, null=True)

    def complete(self):
        if not self.is_completed():
            self.completion = timezone.now()
            self.save()

    def is_completed(self):
        return self.completion is not None

    def get_absolute_url(self):
        return reverse('speisekammer:shopping_list_detail', kwargs={'pk': self.pk})

    @staticmethod
    def create_from_speisekammer(name):
        instance = ShoppingList(name=name, creation=timezone.now())
        instance.save()

        for product in Product.objects.all():
            ShoppingListItem.create_from_product(instance, product)

    def __str__(self):
        return '{0} created on {1}, completed on {2}'.format(
            self.name if self.name is not None else "", self.creation, self.completion
        )


class ShoppingListItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    item_count = models.PositiveIntegerField()
    shopping_list = models.ForeignKey(ShoppingList, related_name="items")

    @staticmethod
    def create_from_product(shopping_list, product):
        instance = ShoppingListItem(product=product, item_count=product.count_difference(), shopping_list=shopping_list)
        instance.save()

    def __str__(self):
        return '{0} x {1} from list {2}'.format(
            self.product.name, self.item_count, self.shopping_list
        )


class CookingRecipe(models.Model):
    name = models.CharField(max_length=200)
    cooking_time = models.DurationField()
    ingredients = models.ManyToManyField(ShoppingListItem)

    def __str__(self):
        return "Recipe {0}".format(self.name)

