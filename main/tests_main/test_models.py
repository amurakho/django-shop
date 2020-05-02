from django.test import TestCase
from django.contrib.auth.models import User
from main import models


def test_product_creation():
    category = models.Category(name='Test cat')
    category.save()
    product = models.Product(name='Test product',
                             price=100,
                             tablet_count=1,
                             description='Test descr',
                             art=1,
                             in_stock=True,
                             category=category,
                             country='UA',
                             form='tablets',
                             count_per_day=1)
    product.save()
    return product


class ImageSaveTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.product = test_product_creation()
        cls.FLIE = '/home/artem/PycharmProjects/bad_shop/media/prod_images/117-kapsuly-s-gialuronovoy-kislotoy-solgar-30-50017933713065.jpg'

    def test_save_right(self):
        models.Image(image=self.FLIE, is_main=True, product=self.product).save()
        models.Image(image=self.FLIE, is_main=False, product=self.product).save()

        images = models.Image.objects.filter(product=self.product, is_main=True)

        self.assertEqual(1, len(images))

    def test_save_wrong(self):
        models.Image(image=self.FLIE, is_main=True, product=self.product).save()
        models.Image(image=self.FLIE, is_main=True, product=self.product).save()

        images = models.Image.objects.filter(product=self.product, is_main=True)

        self.assertEqual(1, len(images))

    def test_delete_with_is_main_one_image(self):
        image = models.Image(image=self.FLIE, is_main=True, product=self.product)
        image.save()

        image.delete()

        all_images = self.product.get_all_images()
        self.assertEqual(len(all_images), 1)
        self.assertEqual(all_images[0].is_main, True)

    def test_delete_with_is_main_two_images(self):
        image_main = models.Image(image=self.FLIE, is_main=True, product=self.product)
        image_main.save()
        image_not = models.Image(image=self.FLIE, is_main=False, product=self.product)
        image_not.save()

        image_main.delete()

        all_images = self.product.get_all_images()
        self.assertEqual(len(all_images), 1)
        self.assertEqual(all_images[0].is_main, True)


class ReviewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.product = test_product_creation()

    def test_review_save(self):
        user = User(username='test_user', email='zxz@i.ua', password='asd123')
        user.save()
        models.Review(rating=3, text='Test text', author=user, product=self.product).save()

        updated_product = models.Product.objects.get(name='Test product')
        self.assertEqual(3, updated_product.mean_review)


class ProductTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.product = test_product_creation()

    def test_with_promotion(self):
        promotion = models.Promotion(start_date='2020-04-09', end_date='2021-04-09', proc=10)
        promotion.save()
        self.product.promotion = promotion
        self.product.save()

        updated_product = models.Product.objects.get(name='Test product')
        self.assertEqual(90, updated_product.price_with_promotion())

        promotion.delete()
        self.product.promotion = None

    def test_without_promotion(self):
        self.assertEqual(100, self.product.price_with_promotion())
