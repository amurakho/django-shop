from django.test import TestCase

from bucket import views


class AddToBucketTest(TestCase):

    def test_create_bucket_add_new_product(self):

        pass

    def test_get_bucket_add_new_product(self):
        pass

    def test_get_bucket_add_count(self):
        pass


class GetProductTest(TestCase):

    def test_get_with_products(self):
        pass

    def test_get_empty_with_session(self):
        pass

    def test_get_empty_without_session(self):
        pass


class DeleteFromBucketTest(TestCase):

    def test_delete_exist(self):
        pass

    def test_delete_error_not_exist(self):
        pass