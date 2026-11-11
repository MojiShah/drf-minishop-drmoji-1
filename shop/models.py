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
    
class Customer(TimeStampMixin):
    # بهتر بود به user model موجود در django متصل می شدیم ولی برای سادگی این کار را نکردیم
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20,blank=True)
    birth_date = models.DateField(blank=True,null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Country(TimeStampMixin):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.name}"
    
class Province(TimeStampMixin):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country,on_delete=models.PROTECT,related_name='provinces')

    def __str__(self):
        return f"{self.name} ({self.country.name})"
    
class City(TimeStampMixin):
    name = models.CharField(max_length=255)
    province = models.ForeignKey(Province,on_delete=models.PROTECT,related_name='cities')

    def __str__(self):
        return f"{self.name} ({self.province.name})"
    
class Address(TimeStampMixin):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='addresses')
    city = models.ForeignKey(City,on_delete=models.PROTECT,related_name='addresses')
    street = models.CharField(max_length=255)
    alley = models.CharField(max_length=255,blank=True)
    building_number = models.SmallIntegerField(validators=[MinValueValidator(1)])
    building_name= models.CharField(max_length=255,blank=True)
    floor = models.SmallIntegerField(validators=[MinValueValidator(0)],blank=True,null=True)
    unit = models.SmallIntegerField(validators=[MinValueValidator(1)],blank=True,null=True)
    zip_code = models.CharField(max_length=10,blank=True,null=True,validators=[MinLengthValidator(10)])
    # چون max_length=10 است و min_length=10 است پس طول کد پستی باید دقیقا 10 باشد

    def __str__(self):
        return f""" {self.customer.first_name} {self.customer.last_name}: {self.street}, {self.city.name}, 
                {self.city.province.name}, {self.city.province.country.name} ---- 
                {self.alley if self.alley else ""}- {self.building_name if self.building_name else ""} .
                """
                
