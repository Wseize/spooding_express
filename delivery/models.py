from django.db import models
from accounts.models import CustomUser
import string
import random

class TypeCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category/', null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category/', null=True, blank=True)

    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class RatingStore(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField()

    class Meta:
        unique_together = ('user', 'store')

    def __str__(self):
        return f'{self.user.username} - {self.store.name} - {self.rating}'
    

    
class NoticeStore(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='notices')
    notice = models.TextField()


    def __str__(self):
        return f'{self.user.username} - {self.store.name} - {self.notice}'
    


class Gouvernorat(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=8, blank=True, null=True) 


    def save(self, *args, **kwargs):
        if not self.pk and not self.password: 
            self.password = self.generate_password(8)
        super().save(*args, **kwargs)


    @staticmethod
    def generate_password(length=8):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(length))
    

    def __str__(self):
        return self.name
        

class Store(models.Model):

    COUNTRY_CHOICES = [
        ('kasserine', 'Kasserine'),
        ('mahdia', 'Mahdia'),
    ]

    GOVERNORATE_CHOICES = {
        'kasserine': [
            ('sbeitla', 'Sbeitla'),
            ('feriana', 'Feriana'),
            ('thala', 'Thala'),
        ],
        'mahdia': [
            ('rejiche', 'Rejiche'),
            ('chebba', 'Chebba'),
            ('sidi_alouane', 'Sidi Alouane'),
        ],
    }

    name = models.CharField(max_length=100)
    category = models.ForeignKey(TypeCategory, related_name='stores', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='category/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    # address = models.CharField(max_length=255)
    available = models.BooleanField(default=True)
    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES, default='kasserine')
    governorate = models.CharField(max_length=20, choices=GOVERNORATE_CHOICES.get('kasserine', []), default='sbeitla')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    password = models.CharField(max_length=8, blank=True, null=True) 
    gouvernorat = models.ForeignKey(Gouvernorat, on_delete=models.CASCADE, blank=True, null=True)    
    percentage = models.IntegerField(default=15)
    

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(rating.rating for rating in ratings) / ratings.count(), 2)
        return None

    def save(self, *args, **kwargs):
        if not self.pk and not self.password: 
            self.password = self.generate_password(8)
        super().save(*args, **kwargs)

    @staticmethod
    def generate_password(length=8):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(length))
    

class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()

    class Meta:
        unique_together = ('user', 'item')

    def __str__(self):
        return f'{self.user.username} - {self.item.name} - {self.rating}'
    


class CatSuppliments(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Suppliment(models.Model):
    title = models.CharField(max_length=100)    
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    categorySuppliments = models.ForeignKey(CatSuppliments, on_delete=models.CASCADE, blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, related_name='items', on_delete=models.CASCADE, null=True, blank=True)
    store = models.ForeignKey(Store, related_name='items', on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='items/', null=True, blank=True)
    available = models.BooleanField(default=True)
    suppliments = models.ManyToManyField(Suppliment, related_name='items')
    personalized = models.BooleanField(default=False)
    percentage_discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name
    
    @property
    def average_rating(self):
        ratings = self.rating_set.all()  
        if ratings.exists():
            return sum(rating.rating for rating in ratings) / ratings.count()
        return None
    

    def save(self, *args, **kwargs):
        if self.percentage_discount:
            self.price = self.price - (self.price * self.percentage_discount / 100)
        super().save(*args, **kwargs)

class DeliveryPerson(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=8, blank=True, null=True) 
    gouvernorat = models.ForeignKey(Gouvernorat, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.password: 
            self.password = self.generate_password(8)
        super().save(*args, **kwargs)

    @staticmethod
    def generate_password(length=8):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(length))

class Order(models.Model):
    
    RECEIVED = 'Received'
    IN_PROGRESS = 'In Progress'
    IN_TRANSIT = 'In Transit'
    COMPLETE = 'Complete'
    CANCELLED = 'Cancelled'
    CONFIRMED = 'Confirmed' 
    RETURNED = 'Returned'

    STATUS_CHOICES = [
        (RECEIVED, 'Received'),
        (IN_PROGRESS, 'In Progress'),
        (IN_TRANSIT, 'In Transit'),
        (COMPLETE, 'Complete'),
        (CANCELLED, 'Cancelled'), 
        (CONFIRMED, 'Confirmed'),
        (RETURNED, 'Returned'),
    ]

    DELIVERY = 'Delivery'
    TAKE_OUT = 'Take Out'
    ON_THE_SPOT = 'On The Spot'

    EAT_CHOICES = [
        (DELIVERY , 'Delivery'),
        (TAKE_OUT , 'Take Out'),
        (ON_THE_SPOT , 'On The Spot'),
    ]

    
    location = models.CharField(max_length=255, blank=True, null=True)
    items = models.ManyToManyField(Item, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=RECEIVED)
    eat = models.CharField(max_length=20, choices=EAT_CHOICES, default=DELIVERY)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    order_id_returned = models.IntegerField(default=0)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    suppliments = models.ManyToManyField(Suppliment, blank=True) 

    def __str__(self):
        return f"{self.quantity} x {self.item.name} from {self.store.name}"

class Publicity(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='publicity/', null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title
    


class CustomerDeliveryForm(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name
    


class CustomerStoreForm(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name