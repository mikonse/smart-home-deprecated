from django.contrib import admin
from . import models

admin.site.register(models.Product)
admin.site.register(models.Barcode)
admin.site.register(models.ShoppingList)
admin.site.register(models.ShoppingListItem)
