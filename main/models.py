from django.db import models
from django.contrib.auth.models import User
from uuslug import slugify
from django_countries.fields import CountryField


class Promotion(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    proc = models.IntegerField()

    def __str__(self):
        return str(self.proc) + '% | ' + str(self.start_date) + '-2020-04-09-' + str(self.end_date)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Product(models.Model):

    TABLET_TYPE = (
        ('tablets', 'tablets'),
    )

    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    tablet_count = models.IntegerField()
    description = models.TextField()
    art = models.CharField(max_length=20, unique=True)
    in_stock = models.BooleanField(default=True)
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    country = CountryField()
    form = models.CharField(choices=TABLET_TYPE, max_length=10)
    count_per_day = models.IntegerField()
    mean_review = models.IntegerField(default=0)

    def price_with_promotion(self):
        if not self.promotion:
            return self.price
        else:
            promotion = self.promotion.proc / 100
            return float(self.price) - float(self.price) * promotion

    def get_review_count(self):
        return len(Review.objects.filter(product=self))

    def get_all_reviews(self):
        return list(Review.objects.filter(product=self))

    def get_main_image(self):
        images = Image.objects.filter(product=self, is_main=True)
        if images:
            return images[0]

    def get_all_images(self):
        return Image.objects.filter(product=self)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Image(models.Model):
    image = models.ImageField(upload_to='prod_images')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)

    def check_any_is_main(self):
        all_images = self.product.get_all_images()
        if any([image for image in all_images if image.is_main]):
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        already_main = self.product.get_main_image()
        if self.check_any_is_main() and self.is_main and already_main != self:
            self.is_main = False
        return super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.is_main:
            all_images = self.product.get_all_images()
            if len(all_images) == 1:
                return

            old_main_image, new_main_image = None, None
            for image in all_images:
                if image.is_main:
                    old_main_image = image
                if not image.is_main and not new_main_image:
                    new_main_image = image
                if old_main_image and new_main_image:
                    break
            old_main_image.is_main = False
            old_main_image.save()
            new_main_image.is_main = True
            new_main_image.save()

        super().delete(using=using, keep_parents=keep_parents)


class ProductInBucket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    full_price = models.FloatField(default=0.)

    def make_full_price(self):
        return float(self.product.price) * float(self.count)

    def save(self, *args, **kwargs):
        self.full_price = self.make_full_price()
        return super().save(*args, **kwargs)


class Bucket(models.Model):
    session_key = models.CharField(max_length=100, null=True)
    products = models.ManyToManyField(ProductInBucket)

    def make_full_data(self):
        price = 0
        count = 0
        for product in self.products.all():
            price += product.product.price
            count += product.count
        return price, count

    def delete(self, using=None, keep_parents=False):
        print('e')
        self.products.remove()
        super().delete(using, keep_parents)


class Order(models.Model):
    bucket = models.ForeignKey(Bucket, on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=50)
    post_number = models.IntegerField()
    phone = models.CharField(max_length=10)
    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=30)


class Review(models.Model):

    rating = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=1000)
    author = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    hover = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        all_reviews = self.product.get_all_reviews()
        all_reviews.append(self)

        import statistics
        self.product.mean_review = statistics.mean([review.rating for review in all_reviews])
        self.product.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:40] + '|' + self.author.username
