from django.test import TestCase
from django.urls import reverse

from basket import views
from main import models as product_models
from main.tests_main.test_models import test_product_creation


class AddToBucketTest(TestCase):

    def setUp(self) -> None:
        self.product = test_product_creation()

    def test_create_bucket_add_new_product(self):
        resp = self.client.post(reverse('to_bucket'), data={'product': self.product.slug,
                                                            'count': 2})
        self.assertRedirects(resp, reverse('product_detail', args=[self.product.slug]))
        bucket = product_models.Bucket.objects.filter(id=1)
        self.assertEqual(len(bucket), 1)
        products_in_bucket = bucket[0].products.all()
        self.assertEqual(len(products_in_bucket), 1)

        product_in_bucket = products_in_bucket[0]
        self.assertEqual(product_in_bucket.product.slug, self.product.slug)
        self.assertEqual(product_in_bucket.count, 2)
        self.assertEqual(product_in_bucket.full_price, 200)

    def test_get_bucket_add_count(self):
        session = self.client.session
        session['basket'] = '1'
        session.save()

        _ = self.client.post(reverse('to_bucket'), data={'product': self.product.slug,
                                                            'count': 2})
        resp = self.client.post(reverse('to_bucket'), data={'product': self.product.slug,
                                                            'count': 3})

        self.assertRedirects(resp, reverse('product_detail', args=[self.product.slug]))
        bucket = product_models.Bucket.objects.filter(id=1)
        self.assertEqual(len(bucket), 1)
        products_in_bucket = bucket[0].products.all()
        self.assertEqual(len(products_in_bucket), 1)

        product_in_bucket = products_in_bucket[0]
        self.assertEqual(product_in_bucket.product.slug, self.product.slug)
        self.assertEqual(product_in_bucket.count, 5)
        self.assertEqual(product_in_bucket.full_price, 500)

    def test_get_bucket_add_new_product(self):
        session = self.client.session
        session['basket'] = '1'
        session.save()

        bucket = product_models.Bucket.objects.create(session_key='1')

        resp = self.client.post(reverse('to_bucket'), data={'product': self.product.slug,
                                                            'count': 3})
        self.assertRedirects(resp, reverse('product_detail', args=[self.product.slug]))
        bucket = product_models.Bucket.objects.all()
        self.assertEqual(len(bucket), 1)
        products_in_bucket = bucket[0].products.all()
        self.assertEqual(len(products_in_bucket), 1)

        product_in_bucket = products_in_bucket[0]
        self.assertEqual(product_in_bucket.product.slug, self.product.slug)
        self.assertEqual(product_in_bucket.count, 3)
        self.assertEqual(product_in_bucket.full_price, 300)


class GetProductTest(TestCase):

    def setUp(self) -> None:
        self.product = test_product_creation()
        self.product_in_bucket = product_models.ProductInBucket.objects.create(product=self.product,
                                                                               count=1)
        self.bucket = product_models.Bucket.objects.create(session_key='1')

    def test_get_with_products(self):
        self.bucket.products.add(self.product_in_bucket)

        session = self.client.session
        session['basket'] = '1'
        session.save()

        resp = self.client.get(reverse('basket'))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['products_in_bucket']), 1)
        product_in_bucket = resp.context['products_in_bucket'][0]
        self.assertEqual(product_in_bucket.product.slug, self.product.slug)

    def test_get_empty_with_session(self):
        session = self.client.session
        session['basket'] = '1'
        session.save()

        resp = self.client.get(reverse('basket'))
        self.assertEqual(resp.status_code, 404)

    def test_get_empty_without_session(self):
        resp = self.client.get(reverse('basket'))
        self.assertEqual(resp.status_code, 404)


class DeleteFromBucketTest(TestCase):

    def setUp(self) -> None:
        self.product = test_product_creation()
        self.product_in_bucket = product_models.ProductInBucket.objects.create(product=self.product,
                                                                               count=1)
        self.bucket = product_models.Bucket.objects.create(session_key='1')

    def test_delete_exist(self):
        session = self.client.session
        session['basket'] = '1'
        session.save()
        self.bucket.products.add(self.product_in_bucket)

        resp = self.client.post(reverse('delete-item'), data=[self.product.slug])

        self.assertEqual(resp.status_code, 200)
        bucket = product_models.Bucket.objects.filter(session_key='1')
        self.assertEqual(len(bucket), 0)


    def test_delete_error_not_exist(self):
        pass