from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
STATE_CHOICES=(
    ('Uttar Pradesh','Uttar Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Bihar','Bihar'),
    ('West Bengal','West Bengal'),
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Rajasthan','Rajasthan'),
    ('Karnataka','Karnataka'),
    ('Gujarat','Gujarat'),
    ('Orissa','Orissa'),
    ('Kerala','Kerala'),
    ('Jharkhand','Jharkhand'),
    ('Assam','Assam'),
    ('Punjab','Punjab'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Haryana','Haryana'),
    ('Delhi','Delhi'),
    ('Jammu and Kashmir','Jammu and Kashmir'),
    ('Uttarakhand','Uttarakhand'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Tripura','Tripura'),
    ('Meghalaya','Meghalaya'),
    ('Manipur','Manipur'),
    ('Nagaland','Nagaland'),
    ('Goa','Goa'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Puducherry','Puducherry'),
    ('Mizoram','Mizoram'),
    ('Chandigarh','Chandigarh'),
    ('Sikkim','Sikkim'),
    ('Andaman and Nicobar Islands','Andaman and Nicobar Islands'),
    ('Dadra and Nagar Haveli','Dadra and Nagar Haveli'),
    ('Daman and Diu','Daman and Diu'),
    ('Lakshadweep','Lakshadweep'),
    ('Telangana','Telangana'),
)
class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=50,default = 'Telangana')

    def __str__(self):
        return str(self.id)#id will generate defaultly
CAT_CHOICES=(
    ('P','Cpesticides'),
    ('F','Fertlizers'),
    ('PE','Pesticides'),
    ('E','Equipment'),
)
class Product(models.Model):
    id=models.IntegerField(primary_key=True)
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=100)
    category=models.CharField(choices=CAT_CHOICES,max_length=2)
    product_image=models.ImageField(upload_to='productimg')
    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price

STATUS_CHOICE=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On Delivery Process','On Delivery Process'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class Orderplaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICE,default='Pending')
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price