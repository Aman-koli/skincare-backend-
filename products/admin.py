from django.contrib import admin
from .models import Category, Product
from django.contrib import admin
from .models import Category, Product, ProductImage
from .models import Category, Product, ProductImage, Review, Wishlist

# ... baaki purana code jaisa hai waisa rehne do ...

admin.site.register(Review)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # ek product add karte waqt 3 image slots dikhenge

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('name', 'original_price', 'discount_price', 'stock', 'category')

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
