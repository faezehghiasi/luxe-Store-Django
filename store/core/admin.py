from django.contrib import admin

from core.models import Product, Category, Comment


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    pass

# ****************************************************************************************************************************
class CategoryAdmin(admin.ModelAdmin):
    pass

# ****************************************************************************************************************************
class CommentAdmin(admin.ModelAdmin):
    pass

# ****************************************************************************************************************************

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)