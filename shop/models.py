from django.db import models
from django.core.validators import MinValueValidator,MinLengthValidator

# Create your models here.
class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        
class Category(TimeStampMixin):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return f"{self.title}"
    
class DisCount(TimeStampMixin):
    amount = models.FloatField(validators=[MinValueValidator(0)])
    code = models.CharField(max_length=255)
    description = models.CharField(max_length=255,blank=True)
    
    def __str__(self):
        if self.description:
            return f"{self.description} (amount : {self.amount})"
        else:
            return f"Discount Amount: {self.amount}"
    
class Product(TimeStampMixin):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name="products")
    dedescription = models.TextField
    slug = models.SlugField(allow_unicode=True) # استفاده از کاراکتر فارسی مجازه
    price = models.DecimalField(max_digits=15,decimal_places=2)
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    discounts = models.ManyToManyField(DisCount,blank=True)
    
    def __str__(self):
        return f"{self.title}: {self.price}"
    
class Comment(TimeStampMixin):
    COMMENT_STATUS_WAITING = "w"
    COMMENT_STATUS_APPROVED = "a"
    COMMENT_STATUS_REJECTED = "r"
    COMMENT_STATUS_CHOICES = [
        (COMMENT_STATUS_WAITING, "Waiting"),
        (COMMENT_STATUS_APPROVED, "Approved"),
        (COMMENT_STATUS_REJECTED, "Rejected"),
    ]
    
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=255)
    text = models.TextField(max_length=5000,validators=[MinLengthValidator(10)])
    status = models.CharField(max_length=1,choices=COMMENT_STATUS_CHOICES,default=COMMENT_STATUS_WAITING)
    
    def __str__(self):
        return f"{self.name}: {self.text[:30]}"
