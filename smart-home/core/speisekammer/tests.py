from django.urls import reverse
from rest_framework import status
from rest_framework import test
from . import models


class ProductAPITests(test.APITestCase):
    fixtures = ['speisekammer/fixtures/speisekammer.json']

    def test_create_product(self):
        """
        Test new account creation
        """
        url = reverse('api:speisekammer:product-list')
        data = {'name': 'Cucumber', 'stock_count': 10}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Product.objects.filter(name='Cucumber').count(), 1)
        self.assertEqual(models.Product.objects.get(name='Cucumber').name, 'Cucumber')
        self.assertEqual(models.Product.objects.get(name='Cucumber').stock_count, 10)

    def test_delete_product(self):
        """
        Test product deletion
        """
        url = reverse('api:speisekammer:product-detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Product.objects.filter(pk=1).exists())

    def test_product_item_io(self):
        """
        Test product item count io calls
        """
        instance_pk = 1

        # Test adding 10 to the item count
        item_io = 10
        url = reverse('api:speisekammer:product-item-io', kwargs={'pk': instance_pk})
        item_count_before = models.Product.objects.get(pk=instance_pk).item_count
        response = self.client.post(url, data={'item_io': item_io})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Product.objects.get(pk=instance_pk).item_count, item_count_before + item_io)

        # Test subtracting 10 again
        item_io = -10
        item_count_before = models.Product.objects.get(pk=instance_pk).item_count
        response = self.client.post(url, data={'item_io': item_io})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Product.objects.get(pk=instance_pk).item_count, item_count_before + item_io)

        # Test subtracting more than in stock
        item_io = -models.Product.objects.get(pk=instance_pk).item_count - 10
        response = self.client.post(url, data={'item_io': item_io})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Product.objects.get(pk=instance_pk).item_count, 0)

    def test_product_stock_io(self):
        """
        Test product stock count io calls
        """
        instance_pk = 1

        # Test adding 10 to the item count
        stock_io = 10
        url = reverse('api:speisekammer:product-stock-io', kwargs={'pk': instance_pk})
        stock_count_before = models.Product.objects.get(pk=instance_pk).stock_count
        response = self.client.post(url, data={'stock_io': stock_io})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Product.objects.get(pk=instance_pk).stock_count, stock_count_before + stock_io)

        # Test subtracting 10 again
        stock_io = -10
        stock_count_before = models.Product.objects.get(pk=instance_pk).stock_count
        response = self.client.post(url, data={'stock_io': stock_io})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Product.objects.get(pk=instance_pk).stock_count, stock_count_before + stock_io)

        # Test subtracting more than in stock
        stock_io = -models.Product.objects.get(pk=instance_pk).stock_count - 10
        response = self.client.post(url, data={'stock_io': stock_io})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Product.objects.get(pk=instance_pk).stock_count, 0)

