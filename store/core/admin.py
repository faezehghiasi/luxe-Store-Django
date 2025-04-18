from django.contrib import admin
from core.models import *

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount', 'quantity', 'enabled', 'category']
    list_filter = ['enabled', 'category']
    search_fields = ['name', 'description']
    list_editable = ['price', 'discount', 'quantity', 'enabled']
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ['category']

# ****************************************************************************************************************************
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'create_date']
    search_fields = ['name']
    prepopulated_fields = {}

# ****************************************************************************************************************************
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'create_date', 'user']
    search_fields = ['name']
    list_filter = ['create_date']
    raw_id_fields = ['user']

# ****************************************************************************************************************************
class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0
    readonly_fields = ['total_price_count']
    fields = ['product', 'count', 'price', 'discount', 'total_price_count']
    raw_id_fields = ['product']

# ****************************************************************************************************************************
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['number', 'user', 'date', 'total_before_discount_in_invoice', 'vat']
    list_filter = ['date']
    search_fields = ['number', 'user__username']
    readonly_fields = ['number', 'date']
    raw_id_fields = ['user', 'address']
    inlines = [InvoiceItemInline]

# ****************************************************************************************************************************
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['date', 'status', 'ref_number', 'total_price', 'invoice']
    list_filter = ['status', 'date']
    search_fields = ['ref_number', 'invoice__number']
    list_editable = ['status']
    readonly_fields = ['ref_number', 'authorization_code', 'invoice', 'description', 'user_ip', 'date']
    raw_id_fields = ['invoice']

# ****************************************************************************************************************************
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'street', 'city', 'postal_code', 'country']
    search_fields = ['user__username', 'street', 'city', 'postal_code']
    list_filter = ['city', 'country']
    raw_id_fields = ['user']

# ****************************************************************************************************************************
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'product', 'count', 'price', 'total_price_count']
    list_filter = ['invoice__date']
    search_fields = ['product__name', 'invoice__number']
    raw_id_fields = ['product', 'invoice']
    readonly_fields = ['total_price_count']

# ****************************************************************************************************************************

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(InvoiceItem, InvoiceItemAdmin)