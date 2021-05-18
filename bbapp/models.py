from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Sum
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
import uuid
from datetime import datetime

FIELD_CHOICES = (
    ('SO', 'Select One'),
    ('ART', 'Arts'),
    ('MSC', 'Music'),
    ('HST', 'History'),
    ('LNG', 'Languages'),
    ('LAW', 'Law'),
    ('PHL', 'Philosophy'),
    ('THE', 'Theology'),
    ('ECN', 'Economics'),
    ('PLS', 'Political Science'),
    ('PSY', 'Psychology'),
    ('SOC', 'Sociology'),
    ('NUR', 'Nursing'),
    ('BIO', 'Biology'),
    ('CHM', 'Chemistry'),
    ('PHY', 'Physics'),
    ('ENG', 'Engineering'),
    ('CSC', 'Computer Science'),
    ('MTH', 'Mathematics'),
    ('BUS', 'Business'),
    ('FIN', 'Finance'),
    ('ACT', 'Accounting'), 
    ('OTH', 'Other'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE) #User deleted? Delete profile
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length = 100, null=True)
    phone = models.CharField(max_length = 10, null=True)
    major = models.CharField(max_length = 100, null=True)
    housing = models.CharField(max_length = 100, null=True)
    field = models.CharField(
        max_length=4, choices=FIELD_CHOICES, default='Select One',
        null=True)  #dropdown
    def __str__(self):
        return self.user.username

class Rating(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    buyerrating = models.FloatField(default=5.00, )
    numberofbuyerratings = models.FloatField(default=1.00)
    sellerrating = models.FloatField(default=5.00)
    numberofsellerratings = models.FloatField(default=1.00)
    def __str__(self):
        return str(self.user.username)+' has a buyer rating of '+str(self.buyerrating)+' and a seller rating of '+str(self.sellerrating)

BOOK_CONDITION_CHOICES = (('SO', 'Select One'), ('NE', 'New'), ('GR', 'Great'),
                          ('GO', 'Good'), ('AV', 'Average'), ('PO', 'Poor'))


SELL_DONATE_CHOICES = (('SO', 'Select One'), ('SE', 'Selling'), ('DO','Donating'))

class Book(models.Model):
    uuid=models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User,default = 1,null = True, on_delete = models.SET_NULL, blank=False)
    image = models.ImageField(upload_to = 'images/', null=True, blank=False)
    selldonate = models.CharField(
        max_length=2,
        choices=SELL_DONATE_CHOICES,
        default='Select One',
        null=True)
    title = models.CharField(max_length=100, null=True)
    author = models.CharField(max_length=100, null=True)
    ISBN13 = models.CharField(max_length=13, null=True)
    ISBN13Conf = models.CharField(max_length=13, null=True)
    edition = models.CharField(max_length=100, null=True)
    condition = models.CharField(
        max_length=2,
        choices=BOOK_CONDITION_CHOICES,
        default='Select One',
        null=True)  #dropdown
    field = models.CharField(
        max_length=4, choices=FIELD_CHOICES, default='Select One',
        null=True)  #dropdown
    price = models.DecimalField(max_digits=100, decimal_places=2, null=True)
    reported = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ["price"]


TRANSACTION_CHOICES = (('Created', 'Created'), ('Pending', 'Pending'), ('Completed','Completed'))

class Transaction(models.Model):
    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    buyer = models.ForeignKey(User,default = 1,null = True, on_delete = models.SET_NULL,related_name='buyer')
    seller = models.ForeignKey(User,default = 1,null = True, on_delete = models.SET_NULL, related_name='seller')
    book = models.ForeignKey(Book,default = 1,null = True, on_delete = models.SET_NULL, related_name='book')
    buyerhasrated = models.BooleanField(default=False)
    sellerhasrated = models.BooleanField(default=False)
    status = models.CharField(max_length=40, default='Created', null=True)
    # def __str__(self):
    #     return "Seller: "+str(self.seller)+", Buyer: "+str(self.buyer)+", Book: "+str(self.book.title)
    def save(self, *args, **kwargs):
        if self.buyerhasrated==False and self.sellerhasrated==False:
            self.status='Created'
        elif self.buyerhasrated or self.sellerhasrated:
            self.status='Pending'
            if self.buyerhasrated and self.sellerhasrated:
                self.status='Completed'
        super(Transaction, self).save(*args, **kwargs)

class Message(models.Model):
    text = models.TextField()
    sender = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='recipient')
    transaction = models.ForeignKey(Transaction, null=True, on_delete=models.CASCADE, related_name='transaction')
    creation_time = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return 'Message: '+str(self.text)

class Cart(models.Model):
    owner = models.OneToOneField(User, on_delete = models.CASCADE, null=True)
    cartitem = models.ManyToManyField(Book)
    @property
    def total(self):
        return self.cartitem.aggregate(Sum('price'))['price__sum'] or 0
    def __str__(self):
        return 'This is the cart for: '+str(self.owner.username)

class Wishlist(models.Model):
    owner = models.OneToOneField(User, on_delete = models.CASCADE, null=True)
    item = models.ManyToManyField(Book)
    @property
    def total(self):
        return self.item.aggregate(Sum('price'))['price__sum'] or 0
    def __str__(self):
        return 'This is the wishlist for: '+str(self.owner.username)

class Reported(models.Model):
    #report_id = models.AutoField(auto_created = True, primary_key = True, null = False)
    #reporter = models.ForeignKey(User, on_delete = models.CASCADE,related_name='reporter')
    #reported = models.ForeignKey(User, on_delete = models.CASCADE, related_name='reported')
    #uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    reporter = models.ForeignKey(User,default = 1,null = True, on_delete = models.SET_NULL,related_name='reporter')
    reported = models.ForeignKey(User,default = 1,null = True, on_delete = models.SET_NULL, related_name='reported')
    resolved = models.BooleanField(default = False)
    reportedtransaction = models.ForeignKey(Transaction, null=True, on_delete=models.SET_NULL)
    reportedbook = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL, related_name='reportedbook')

    def __str__(self):
        return str(self.reporter)+' has reported '+str(self.reported)