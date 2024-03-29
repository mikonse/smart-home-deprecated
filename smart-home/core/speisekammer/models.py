from django.utils import timezone
from django.db import models
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    stock_count = models.PositiveIntegerField(default=0)
    item_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['name']

    def assign_barcode(self, barcode):
        barcode = Barcode(product=self, barcode=barcode)
        barcode.save()

    def to_active_list(self, amount):
        active_list = ShoppingList.get_active_list()
        active_list.add_item(self, amount)

    @staticmethod
    def item_io_by_barcode(io, barcode):
        if not Barcode.objects.filter(barcode=barcode).exists():
            return False
        product = Barcode.objects.get(barcode=barcode).product
        return product.item_io(io)

    def stock_io(self, io):
        if type(io) == str:
            try:
                io = int(io)
            except ValueError:
                return False

        self.stock_count += io
        if self.stock_count < 0:
            self.stock_count = 0
        self.save()
        return True

    def item_io(self, io):
        if type(io) == str:
            try:
                io = int(io)
            except ValueError:
                return False

        self.item_count += io
        if self.item_count < 0:
            self.item_count = 0
        self.save()
        return True

    def count_difference(self):
        return self.stock_count - self.item_count if self.stock_count > self.item_count else 0

    def get_absolute_url(self):
        return reverse('api:speisekammer:product-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Barcode(models.Model):
    product = models.ForeignKey(Product, related_name='barcodes', on_delete=models.CASCADE)
    barcode = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('api:speisekammer:barcode-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.barcode


class ShoppingList(models.Model):
    name = models.CharField(max_length=100, blank=True)
    creation = models.DateTimeField()
    completion = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=False)

    def get_name(self):
        if self.name is None or self.name == '':
            return "Unnamed list %d" % self.pk
        else:
            return self.name

    @staticmethod
    def get_active_list():
        if not ShoppingList.objects.filter(active=True).exists():
            if ShoppingList.objects.exclude(completion__isnull=True).exists():
                shopping_list = ShoppingList.create_from_speisekammer(name='')
            else:
                shopping_list = ShoppingList.objects.filter(completion__isnull=False).order_by('creation')[0]
            shopping_list.active = True
            shopping_list.save()
        else:
            shopping_list = ShoppingList.objects.filter(active=True).order_by('creation')[0]
        return shopping_list

    def add_item(self, product, item_count=0):
        if type(item_count) == str:
            try:
                item_count = int(item_count)
            except ValueError:
                return False

        if ShoppingListItem.objects.filter(shopping_list=self, product=product).exists():
            item = ShoppingListItem.objects.filter(shopping_list=self, product=product)[0]
            item.item_count += item_count
        else:
            item = ShoppingListItem(shopping_list=self, product=product, item_count=item_count)
        item.save()
        return True

    def update_from_speisekammer(self):
        for item in self.items:
            item.update_from_speisekammer()
        if not ShoppingListItem.objects.filter(shopping_list=self, item_count__gt=0).exists():
            self.complete()
            return True
        return False

    def complete(self):
        if not self.is_completed():
            self.completion = timezone.now()
            self.active = False
            for item in self.items.all():
                item.complete()
            self.save()

    def is_completed(self):
        return self.completion is not None

    def get_absolute_url(self):
        return reverse('api:speisekammer:shoppinglist-detail', kwargs={'pk': self.pk})

    @staticmethod
    def create_from_speisekammer(name):
        instance = ShoppingList(name=name, creation=timezone.now())
        instance.save()

        for product in Product.objects.all():
            ShoppingListItem.create_from_product(instance, product)
        return instance

    def __str__(self):
        return '{0} created on {1}, completed on {2}'.format(
            self.name if self.name is not None else "", self.creation, self.completion
        )


class ShoppingListItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    item_count = models.PositiveIntegerField(default=0)
    shopping_list = models.ForeignKey(ShoppingList, related_name="items")
    done = models.BooleanField(default=False)

    class Meta:
        unique_together = ('product', 'shopping_list')

    def update_from_speisekammer(self):
        self.item_count = self.product.count_difference()
        self.save()

    def complete(self):
        self.product.item_io(self.item_count)
        self.done = True
        self.save()

    def item_io(self, io):
        if type(io) == str:
            try:
                io = int(io)
            except ValueError:
                return False

        self.item_count += io
        if self.item_count < 0:
            self.item_count = 0
        self.save()
        return True

    @staticmethod
    def create_from_product(shopping_list, product):
        if product.count_difference() > 0:
            instance = ShoppingListItem(
                product=product,
                item_count=product.count_difference(),
                shopping_list=shopping_list
            )
            instance.save()
            return True
        else:
            return False

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

