from datetime import datetime

from django.db import models
from django.utils.text import slugify
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

# ****************************************************************************************************************************
class Base(models.Model):
    create_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    deleted = models.BooleanField(default=False)
    deleted_date = models.DateField(default=None, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        abstract = True

# ****************************************************************************************************************************
class Category(Base):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

# ****************************************************************************************************************************
class Product(Base):
    name = models.CharField(max_length=300)
    price = models.IntegerField(default=0)
    discount = models.FloatField(default=0)
    enabled = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)
    quantity = models.IntegerField(default=0)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products')
    image = models.ImageField(upload_to='covers/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# ****************************************************************************************************************************
class Comment(Base):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


# ****************************************************************************************************************************
class Invoice(models.Model):

    date = models.DateField(auto_now_add=True)
    number = models.CharField(max_length=100,null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    address = models.ForeignKey('Address', on_delete=models.PROTECT, related_name='invoices')  # flexible relation
    total_before_discount_in_invoice = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    vat = models.FloatField(default=0.09)

    def save(self, *args, **kwargs):
        if not self.number:
            # Generate invoice number on first save
            year_month = datetime.now().strftime('%Y%m')
            last_invoice = Invoice.objects.filter(
                number__startswith=f'INV{year_month}'
            ).order_by('-number').first()

            if last_invoice:
                last_seq = int(last_invoice.number[-5:])
                new_seq = last_seq + 1
            else:
                new_seq = 1

            self.number = f'INV{year_month}{new_seq:05d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice #{self.number or 'N/A'} - {self.user.username}"

# ****************************************************************************************************************************
class InvoiceItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    discount = models.FloatField(default=0)
    name = models.CharField(max_length=300)
    total_price_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.invoice.number} - {self.product.name}"


# ****************************************************************************************************************************
class Payment(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_DONE = 'done'
    STATUS_ERROR = 'error'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_DONE, 'Done'),
        (STATUS_ERROR, 'Error'),
    )
    date = models.DateField(auto_now_add=True)
    invoice = models.OneToOneField(Invoice, on_delete=models.PROTECT)
    total_price = models.IntegerField(default=0)
    ref_number = models.CharField(max_length=300, null=True, blank=True)# کد رهگیری تراکنش
    authorization_code = models.CharField(max_length=300)
    description = models.TextField()
    user_ip = models.CharField(max_length=300)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default=STATUS_PENDING)

    def __str__(self):
        return f"Payment for Invoice #{self.invoice.number or 'N/A'}, User : {self.invoice.user.username}"

# ****************************************************************************************************************************
class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='Iran')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.street}, {self.city}"
