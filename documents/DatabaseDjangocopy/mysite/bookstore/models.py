from django.db import models
from django.core import validators

# Create your models here.
# class Book(models.Model):
# 	title = models.CharField(max_length=20)
# 	pub_date = models.DateTimeField('date published')
# 	isbn = models.CharField(max_length=14)

class Customer(models.Model):
    login_name = models.CharField(max_length = 16, primary_key = True)
    pwd = models.CharField(max_length = 8)
    surname = models.CharField(max_length = 16)
    given_name = models.CharField(max_length = 64)
    credit_card = models.CharField(max_length = 16)
    address = models.CharField(max_length = 128)
    phoneno = models.IntegerField()


class Book(models.Model):
    formats = (("H", "Hardcover"), ("S", "Softcover"))
    isbn = models.CharField(max_length = 14, primary_key = True)
    title = models.CharField(max_length = 128, null = True)
    desc = models.TextField(null = True)
    img = models.URLField(null = True)
    author = models.CharField(max_length = 128, null = True)
    frmt = models.CharField(max_length = 1, choices = formats, null = True)
    publisher = models.CharField(max_length = 64, null = True)
    yr = models.IntegerField(null = True, validators = [validators.MinValueValidator(0, "Year cannot be less than 0!")])
    sbj = models.CharField(max_length = 64, null = True)
    keywords = models.CharField(max_length = 128, null = True)
    price = models.FloatField(null = True)
    copies = models.IntegerField(null = False, default = 0)
   


class Ord(models.Model):
    oid = models.AutoField(primary_key = True)
    book = models.ForeignKey(Book)
    customer = models.ForeignKey(Customer)
    timestmp = models.DateTimeField(null = True)
    stat = models.CharField(max_length = 16, null = True)
    qty = models.IntegerField(null = False,
                              default = 0,
                              validators = [validators.MinValueValidator(0, "Order quantity cannot be negative.")])



class Opinion(models.Model):
    customer = models.ForeignKey(Customer)
    book = models.ForeignKey(Book)
    score = models.IntegerField(validators = [validators.MinValueValidator(0, "Score must be >= 0."), validators.MaxValueValidator(10, "Score must be <= 10.")], default = 0)
    txt = models.TextField(default = "A")

    class Meta:
        unique_together = ("customer", "book")


class Rate(models.Model):
    rater = models.ForeignKey(Customer)
    opinion = models.ForeignKey(Opinion)
    rating = models.IntegerField(default = 0, validators = [validators.MinValueValidator(0, "Rating must be >= 0."), validators.MaxValueValidator(2, "Rating must be <= 2.")])

    class Meta:
        unique_together = ("rater", "opinion")