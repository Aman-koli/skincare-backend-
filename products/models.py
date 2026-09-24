from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    original_price = models.DecimalField(max_digits=10, decimal_places=2)  # purana price (cut wala)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # naya price
    
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    skin_type = models.CharField(
        max_length=50,
        choices=[
            ("all", "All Skin Types"),
            ("oily", "Oily"),
            ("dry", "Dry"),
            ("sensitive", "Sensitive"),
            ("combination", "Combination"),
        ],
        default="all",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def discount_percentage(self):
        if self.discount_price and self.original_price:
            return round(((self.original_price - self.discount_price) / self.original_price) * 100)
        return 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f"{self.product.name} - Image"



class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # ek user, ek product pe sirf ek review

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # ek user, ek product ek baar hi wishlist me

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

    