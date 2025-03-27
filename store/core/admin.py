from django.contrib import admin

from core.models import Product, Category, Tag, Comment, Like


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    pass

# ****************************************************************************************************************************
class CategoryAdmin(admin.ModelAdmin):
    pass

# ****************************************************************************************************************************
class TagAdmin(admin.ModelAdmin):
    pass

# ****************************************************************************************************************************
class CommentAdmin(admin.ModelAdmin):
    pass


# ****************************************************************************************************************************
class LikeAdmin(admin.ModelAdmin):
    pass

# ****************************************************************************************************************************

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)