from django.test import TestCase
from django.forms.models import inlineformset_factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files import File
from django.contrib.messages import get_messages

from main import models, admin

IMAGE_FILE = '/home/artem/PycharmProjects/bad_shop/static/img/image_for_test.png'


class MockRequest:
    pass


class AdminModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = models.Category(name='test_cat')
        cls.category.save()

        cls.ProductFormSet = inlineformset_factory(
            models.Product, models.Image, formset=admin.ImageInlineFormset,
            exclude=()
        )

        cls.http_request = HttpRequest()
        cls.http_request.user = User.objects.create_superuser(username='test',
                                                              password='test123',
                                                              email='asd@i.ua',
                                                              )

        middleware = SessionMiddleware()
        middleware.process_request(cls.http_request)
        cls.http_request.session.save()

        middleware = MessageMiddleware()
        middleware.process_request(cls.http_request)
        cls.http_request.session.save()

    def setUp(self) -> None:
        upload_file = open(IMAGE_FILE, 'rb')
        self.IMAGE_DATA = {
            'image_set-0-image': SimpleUploadedFile(upload_file.name, upload_file.read(), 'application/png')
        }

        self.ID = 99

        self.PROD = models.Product.objects.create(name='test',
                                                 price=1.,
                                                 tablet_count=1,
                                                 description='asd',
                                                 art='test123',
                                                 slug='test',
                                                 category=self.category,
                                                 country='BH',
                                                 form='tablets',
                                                 count_per_day=1,
                                                 id=self.ID)

        self.WITHOUT_IMAGE_DATA = {
            'image_set-TOTAL_FORMS': 3,
            'image_set-INITIAL_FORMS': 0,
            'image_set-MIN_NUM_FORMS': 0,
            'image_set-MAX_NUM_FORMS': 1000,
        }

        self.IMAGE_WITHOUT_MAIN = {
            'image_set-0-id': '',
            'image_set-0-product': self.ID,
        }

        self.IS_MAIN = {
            'image_set-0-is_main': True,
        }

    def test_valid(self):
        data = self.WITHOUT_IMAGE_DATA.copy()
        data.update(self.IMAGE_WITHOUT_MAIN)
        data.update(self.IS_MAIN)

        formset = self.ProductFormSet(data, self.IMAGE_DATA, instance=self.PROD)
        self.assertEqual(formset.is_valid(), True)

    def test_without_image(self):
        data = self.WITHOUT_IMAGE_DATA.copy()
        formset = self.ProductFormSet(data, instance=self.PROD)

        self.assertEqual(formset.is_valid(), False)
        self.assertEqual(formset.non_form_errors()[0], 'Нужно ввести хотя бы одно изображение')

    def test_without_is_main_one_image(self):
        data = self.WITHOUT_IMAGE_DATA.copy()
        data.update(self.IMAGE_WITHOUT_MAIN)
        data['image_set-0-is_main'] = False

        formset = self.ProductFormSet(data, self.IMAGE_DATA, instance=self.PROD)
        formset.is_valid()

        my_modeladmin = admin.ProductAdmin(admin_site=AdminSite(), model=models.Product)
        my_modeladmin.save_related(request=self.http_request, form=None, formsets=[formset], change=False)

        product = models.Product.objects.get(id=self.ID)
        self.assertEqual(True if product else False, True)
        images = product.get_all_images()
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0].is_main, True)

    def test_without_is_main_two_images(self):
        data = self.WITHOUT_IMAGE_DATA.copy()
        data.update(self.IMAGE_WITHOUT_MAIN)
        data.update({
            'image_set-0-is_main': False,
        })

        data.update({
            'image_set-1-id': '',
            'image_set-1-product': self.ID,
            'image_set-1-is_main': False
        })
        upload_file = open(IMAGE_FILE, 'rb')
        image_data = self.IMAGE_DATA.copy()
        image_data.update({
            'image_set-1-image': SimpleUploadedFile(upload_file.name, upload_file.read(), 'application/png')
        })

        formset = self.ProductFormSet(data, image_data, instance=self.PROD)

        my_modeladmin = admin.ProductAdmin(admin_site=AdminSite(), model=models.Product)
        my_modeladmin.save_related(request=self.http_request, form=None, formsets=[formset], change=False)

        product = models.Product.objects.get(id=self.ID)
        self.assertEqual(True if product else False, True)

        images = product.get_all_images()
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0].is_main, True)
        self.assertEqual(images[1].is_main, False)

    def test_with_is_main_two_images_first(self):
        data = self.WITHOUT_IMAGE_DATA.copy()
        data.update(self.IMAGE_WITHOUT_MAIN)
        data.update(self.IS_MAIN)

        data.update({
            'image_set-1-id': '',
            'image_set-1-product': self.ID,
            'image_set-1-is_main': False,
        })
        upload_file = open(IMAGE_FILE, 'rb')
        image_data = self.IMAGE_DATA.copy()
        image_data.update({
            'image_set-1-image': SimpleUploadedFile(upload_file.name, upload_file.read(), 'application/png')
        })

        formset = self.ProductFormSet(data, image_data, instance=self.PROD)

        my_modeladmin = admin.ProductAdmin(admin_site=AdminSite(), model=models.Product)
        my_modeladmin.save_related(request=self.http_request, form=None, formsets=[formset], change=False)

        product = models.Product.objects.get(id=self.ID)
        self.assertEqual(True if product else False, True)
        images = product.get_all_images()
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0].is_main, True)
        self.assertEqual(images[1].is_main, False)

    def test_with_is_main_two_images_second(self):
        data = self.WITHOUT_IMAGE_DATA.copy()
        data.update(self.IMAGE_WITHOUT_MAIN)
        data.update({
            'image_set-0-is_main': False,
        })

        data.update({
            'image_set-1-id': '',
            'image_set-1-product': self.ID,
            'image_set-1-is_main': True,
        })
        upload_file = open(IMAGE_FILE, 'rb')
        image_data = self.IMAGE_DATA.copy()
        image_data.update({
            'image_set-1-image': SimpleUploadedFile(upload_file.name, upload_file.read(), 'application/png')
        })

        formset = self.ProductFormSet(data, image_data, instance=self.PROD)
        self.assertEqual(formset.is_valid(), True)

        my_modeladmin = admin.ProductAdmin(admin_site=AdminSite(), model=models.Product)
        my_modeladmin.save_related(request=self.http_request, form=None, formsets=[formset], change=False)

        product = models.Product.objects.get(id=self.ID)
        self.assertEqual(True if product else False, True)
        images = product.get_all_images()
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0].is_main, False)
        self.assertEqual(images[1].is_main, True)

    def test_with_is_main_two_images_both(self):
        data = self.WITHOUT_IMAGE_DATA.copy()
        data.update(self.IMAGE_WITHOUT_MAIN)
        data.update({
            'image_set-0-is_main': True,
        })

        data.update({
            'image_set-1-id': '',
            'image_set-1-product': self.ID,
            'image_set-1-is_main': True,
        })
        upload_file = open(IMAGE_FILE, 'rb')
        image_data = self.IMAGE_DATA.copy()
        image_data.update({
            'image_set-1-image': SimpleUploadedFile(upload_file.name, upload_file.read(), 'application/png')
        })

        formset = self.ProductFormSet(data, image_data, instance=self.PROD)

        my_modeladmin = admin.ProductAdmin(admin_site=AdminSite(), model=models.Product)
        my_modeladmin.save_related(request=self.http_request, form=None, formsets=[formset], change=False)

        images = models.Product.objects.get(id=self.ID).get_all_images()
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0].is_main, True)
        self.assertEqual(images[1].is_main, False)

    def test_delete_all_images(self):
        data = self.WITHOUT_IMAGE_DATA.copy()
        data.update(self.IMAGE_WITHOUT_MAIN)
        data['image_set-0-id'] = self.ID
        data['image_set-1-id'] = self.ID
        data['image_set-0-DELETE'] = True
        data['image_set-1-DELETE'] = True
        data['image_set-__prefix__-product'] = self.ID
        data['image_set-0-is_main'] = True

        upload_file = open(IMAGE_FILE, 'rb')
        image_data = self.IMAGE_DATA.copy()
        image_data.update({
            'image_set-1-image': SimpleUploadedFile(upload_file.name, upload_file.read(), 'application/png')
        })

        formset = self.ProductFormSet(data, image_data, instance=self.PROD)

        self.assertEqual(formset.is_valid(), False)
        self.assertEqual(formset.non_form_errors()[0], 'Ты пытался удалить все изображения. '
                                                       'Загрузи заранее новое, которое будет главным. '
                                                       'Изменения не сохранились')

    # def test_delete_valid(self):
    #     data = self.WITHOUT_IMAGE_DATA.copy()
    #     data.update(self.IMAGE_WITHOUT_MAIN)
    #     data['image_set-0-id'] = self.f_image.id
    #     data['image_set-1-id'] = self.s_image.id
    #     data['image_set-0-DELETE'] = False
    #     data['image_set-1-DELETE'] = True
    #     data['image_set-__prefix__-product'] = self.ID
    #     data['image_set-0-is_main'] = True
    #     data['image_set-1-is_main'] = False
    #
    #     upload_file = open(IMAGE_FILE, 'rb')
    #     image_data = self.IMAGE_DATA.copy()
    #     image_data.update({
    #         'image_set-1-image': SimpleUploadedFile(upload_file.name, upload_file.read(), 'application/png')
    #     })
    #     formset = self.ProductFormSet(data, image_data, instance=self.PROD)
    #
    #     self.assertEqual(formset.is_valid(), True)
    #
    #     my_modeladmin = admin.ProductAdmin(admin_site=AdminSite(), model=models.Product)
    #     my_modeladmin.save_related(request=self.http_request, form=None, formsets=[formset], change=False)
    #
    #     images = self.PROD.get_all_images()
    #     self.assertEqual(len(images), 1)
    #     self.assertEqual(images[0].is_main, True)

    # def test_delete_with_is_main_one_image(self):
    #     prod = models.Product.objects.get(id=self.ID)
    #
    #     image = models.Image(product=prod, is_main=True, id=self.ID)
    #     image.image.save('image_for_test.png', File(open(IMAGE_FILE, 'rb')))
    #     image.save()
    #
    #     data = self.WITHOUT_IMAGE_DATA.copy()
    #     data.update(self.IMAGE_WITHOUT_MAIN)
    #     data['image_set-0-id'] = self.ID
    #     data['image_set-0-DELETE'] = True
    #     data['image_set-__prefix__-product'] = self.ID
    #     data.update(self.IS_MAIN)
    #     formset = self.ProductFormSet(data, self.IMAGE_DATA, instance=self.PROD)
    #
    #     my_modeladmin = admin.ProductAdmin(admin_site=AdminSite(), model=models.Product)
    #     my_modeladmin.save_related(request=self.http_request, form=None, formsets=[formset], change=False)
    #
    #     images = models.Product.objects.get(id=self.ID).get_all_images()
    #     self.assertEqual(len(images), 1)
    #     self.assertEqual(images[0].is_main, True)


    # def test_delete_with_is_main_two_images(self):
    #     prod = models.Product.objects.get(id=self.ID)
    #
    #     image = models.Image(product=prod, is_main=True, id=self.ID)
    #     image.image.save('image_for_test.png', File(open(IMAGE_FILE, 'rb')))
    #     image.save()
    #
    #     image = models.Image(product=prod, is_main=True, id=self.ID)
    #     image.image.save('image_for_test.png', File(open(IMAGE_FILE, 'rb')))
    #     image.save()
    #
    #     data = self.WITHOUT_IMAGE_DATA.copy()
    #     data['image_set-TOTAL_FORMS'] = 2
    #     data.update(self.IMAGE_WITHOUT_MAIN)
    #     data['image_set-0-id'] = self.ID
    #     data['image_set-1-id'] = self.ID
    #     data['image_set-0-DELETE'] = True
    #     data['image_set-__prefix__-product'] = self.ID
    #     data.update(self.IS_MAIN)
    #
    #     upload_file = open('/home/artem/PycharmProjects/bad_shop/static/img/image_for_test.png', 'rb')
    #     image_data = self.IMAGE_DATA.copy()
    #     image_data.update({
    #         'image_set-1-image': SimpleUploadedFile(upload_file.name, upload_file.read(), 'application/png')
    #     })
    #
    #     formset = self.ProductFormSet(data, image_data, instance=self.PROD)
    #
    #     self.assertEqual(formset.is_valid(), True)
    #     formset.save()
    #     #
    #     images = prod.get_all_images()
    #     self.assertEqual(len(images), 1)
    #     self.assertEqual(images[0].is_main, True)

    # def test_delete_valid(self):
    #     prod = models.Product.objects.get(id=self.ID)
    #
    #     image = models.Image(product=prod, is_main=True, id=self.ID)
    #     image.image.save('image_for_test.png', File(open(IMAGE_FILE, 'rb')))
    #     image.save()
    #
    #     image = models.Image(product=prod, is_main=True, id=self.ID)
    #     image.image.save('image_for_test.png', File(open(IMAGE_FILE, 'rb')))
    #     image.save()
    #
    #
    #     data = self.WITHOUT_IMAGE_DATA.copy()
    #     data['image_set-TOTAL_FORMS'] = 2
    #     data.update(self.IMAGE_WITHOUT_MAIN)
    #     data['image_set-0-id'] = self.ID
    #     data['image_set-1-id'] = self.ID
    #     data['image_set-1-DELETE'] = True
    #     data['image_set-__prefix__-product'] = self.ID
    #     data['image_set-0-is_main'] = True
    #
    #     upload_file = open('/home/artem/PycharmProjects/bad_shop/static/img/image_for_test.png', 'rb')
    #     image_data = self.IMAGE_DATA.copy()
    #     image_data.update({
    #         'image_set-1-image': SimpleUploadedFile(upload_file.name, upload_file.read(), 'application/png')
    #     })
    #
    #     formset = self.ProductFormSet(data, image_data, instance=self.PROD)
    #
    #     self.assertEqual(formset.is_valid(), True)
    #     formset.save()
    #     #
    #     images = prod.get_all_images()
    #     self.assertEqual(len(images), 1)
    #     self.assertEqual(images[0].is_main, True)
