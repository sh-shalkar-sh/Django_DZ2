from django.db import models


class Client(models.Model):
    name_client = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=100)

    def __str__(self):
        #return f'name: {self.name_client}, email: {self.email},  phone: {self.phone_number}, address: {self.address}'
        return self.name_client

class Product(models.Model):
    name_product = models.CharField(max_length=50)
    description_product = models.TextField()
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    date_add_product = models.DateField(auto_now_add=True)
    image_product = models.ImageField(upload_to="images/")

    def __str__(self):
        #return f'Product: {self.name_product},  quantity: {self.quantity}, cost: {self.cost},  description: {self.description_product}, product creation date: {self.date_add_product},  image: {self.image_product}'
        return self.name_product







class Order(models.Model):
    buyer = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)                                              #создается автоматически таблица Order_products связи таблиц Order и Product
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    date_create_order = models.DateField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        #return f'name_of_client: {self.buyer.name_client} \nproducts: {self.products.all()} \ntotal_cost: {self.total_cost} \ndate_create_order: {self.date_create_order}'
        return f' №Заказа: {self.id}  от {self.date_create_order }  клиент: {self.buyer.name_client }'





