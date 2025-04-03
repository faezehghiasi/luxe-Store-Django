from django.db import models
from django.utils.text import slugify
import uuid
# from django.contrib.auth.models import User
# from account.models import User #using my user model
from django.contrib.auth import get_user_model
User = get_user_model()


class Base(models.Model):
    create_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4) #for security #for default we sent function not value
    deleted = models.BooleanField(default=False)
    deleted_date = models.DateField(default=None, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        abstract = True
#****************************************************************************************************************************
class Product(Base):
    
    # STATUS_ENABLED = 0
    # STATUS_DISABLED = 1
    # STATUS_DELETED = 2
    # STATUS_CHOICES = ((STATUS_ENABLED,'Enabled'),(STATUS_DISABLED , 'Disabled') , (STATUS_DELETED , 'Deleted'))

    name = models.CharField(max_length=300)
    price = models.IntegerField(default=0)
    discount = models.FloatField(default=0)
    enabled = models.BooleanField(default=True)
    slug = models.SlugField()
    quantity = models.IntegerField(default=0)
    # In web development and content management, a slug is the part of a URL that identifies a specific page or post on a website in a human-readable format. It usually comes after the domain name and helps users and search engines understand the content of the page.
    # Example:
    # URL: https://example.com/blog/what-is-a-slug
    # Slug: what-is-a-slug
    # status = models.IntegerField(max_length=10, choices=STATUS_CHOICES, default=STATUS_ENABLED)


    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='covers/', null=True, blank=True)

    # old_category = models.ForeignKey('Category',on_delete=models.PROTECT,related_name='old_products')
    #این اسم هایی که میدیم برای رابطه های معکوس است که جنگو خودش درست میکند اگه اسم بش ندیم دوتا اسم یکسان درست میکنه و ارور میده موقع مایگریت کردن
    #if we enter argument in '' we can declare class later

    def __str__(self):
        return self.name

#****************************************************************************************************************************
class Category(Base):
    name = models.CharField(max_length=300)
    #product_set = QuerySet //برای رابطه ی معکوس

    def __str__(self):
        return self.name


#****************************************************************************************************************************
class Tag(Base):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


#****************************************************************************************************************************
class Comment(Base):
    name = models.CharField(max_length=300)

    def __str__(self):
       return self.name

#****************************************************************************************************************************
class Like(Base):

    pass

#****************************************************************************************************************************
class InvoiceItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    discount = models.FloatField(default=0)
    name = models.CharField(max_length=300)
    total_price_count = models.IntegerField(default=0)

#****************************************************************************************************************************
class Invoice(models.Model):
    date = models.DateField(auto_now_add=True)

    number = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    total_before_discount_in_invoice = models.IntegerField(default=0)
    discount = models.FloatField(default=0)
    description = models.TextField(null=True, blank=True)
    address = models.TextField()
    vat = models.FloatField(default=0.09)


#****************************************************************************************************************************
class Payment(models.Model):
     STATUS_PENDING = 'pending'
     STATUS_DONE = 'done'
     STATUS_ERROR = 'error'

     STATUS_CHOICES = ((STATUS_PENDING, 'Pending'),(STATUS_DONE, 'Done'),(STATUS_ERROR, 'Error'),(STATUS_DONE, 'done'))
     invoice = models.OneToOneField(Invoice, on_delete=models.PROTECT)
     total_price = models.IntegerField(default=0)
     ref_number = models.CharField(max_length=300, null=True, blank=True)
     authorization_code = models.CharField(max_length=300)
     description = models.TextField()
     user_ip = models.CharField(max_length=300)
     status = models.CharField(choices=STATUS_CHOICES, max_length=20,default=STATUS_PENDING)

#****************************************************************************************************************************


