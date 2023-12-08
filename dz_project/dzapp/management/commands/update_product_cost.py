from django.core.management.base import BaseCommand
from shop_app.models import Product


class Command(BaseCommand):
    help = "update product cost by id product"

    def add_arguments(self, parser):
        parser.add_argument('pk', type=int, help='id of products')
        parser.add_argument("cost", type=float, help="price of product")

    def handle(self, *args, **kwargs):
        pk = kwargs.get('pk')
        cost = kwargs.get('cost')
        product = Product.objects.filter(pk=pk).first()
        product.cost = cost
        product.save()
        self.stdout.write(f'{product}')