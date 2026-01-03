from django.contrib import admin

# Register your models here.
from .models import Category, Product, ProductImage, Variation


class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    search_fields = ['title', 'description']
    list_display = ['__str__', 'price', 'active', 'updated']
    list_editable = ['price', 'active']
    list_filter = ['price', 'active']
    readonly_fields = ['updated', 'timestamp']
    prepopulated_fields = {'slug': ('title',)}
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage)

admin.site.register(Variation)

admin.site.register(Category)
