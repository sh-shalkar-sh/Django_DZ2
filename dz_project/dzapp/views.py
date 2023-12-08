from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
import logging
from dzapp.models import Client, Order, Product
from datetime import datetime, timedelta
from django.core.files.storage import FileSystemStorage
from .forms import ProductForm, ChoiceProductById, ChoiceProductByClientBydays
from django.shortcuts import render, get_object_or_404, redirect

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'dzapp/index.html')


# вывод всех товаров
def products(request):
    products = Product.objects.all()
    logger.info(f'Страница "Список продуктов" успешно открыта')
    return render(request, 'dzapp/products.html', {'products': products})


# вывод списка всех клиентов
def clients(request):
    clients = Client.objects.all()

    logger.info(f'Страница "Список клиентов" успешно открыта')
    return render(request, 'dzapp/clients.html', {'clients': clients})


# вывод заказа по  id
def order(request, id_order: int):
    # order = Order.objects.filter(pk=id_order).first()
    order = Order.objects.get(pk=id_order)
    context = {
        'order': order
    }
    return render(request, 'dzapp/order.html', context=context)


# вывод списка заказов
def orders(request):
    products_all = []
    orders = Order.objects.all()

    context = {
        'orders': orders
    }
    return render(request, 'dzapp/orders_all.html', context=context)


def client_orders(request, id_client: int):
    products = {}

    client = Client.objects.filter(pk=id_client).first()
    orders = Order.objects.filter(buyer=client).all()

    for order in orders:
        products[order.id] = str(order.products.all()).replace('<QuerySet [<', '').replace('>]>', '').split('>, <')

    return render(request, 'dzapp/client_orders.html', {'client': client, 'orders': orders, 'products': products})


def product(request, id_product: int):
    product = Product.objects.filter(pk=id_product).first()
    context = {
        "product": product

    }
    return render(request, "dzapp/product.html", context=context)


def client_products_sorted(request, id_client: int, days: int):
    products = []
    product_set = []
    now = datetime.now()
    before = now - timedelta(days=days)
    client = Client.objects.filter(pk=id_client).first()
    orders = Order.objects.filter(buyer=client, date_create_order__range=(before, now)).all()
    for order in orders:
        products = order.products.all()
        for product in products:
            if product not in product_set:
                product_set.append(product)

    return render(request, 'dzapp/client_all_products_from_orders.html',
                  {'client': client, 'product_set': product_set, 'days': days})


# представление для ввода данных о продукте через форму и сохранение изображения продукта на сервер
def product_form(request, id_product: int):
    product = get_object_or_404(Product, pk=id_product)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product.name_product = request.POST["name_product"]
            product.description_product = request.POST["description_product"]
            product.cost = request.POST["cost"]
            product.quantity = request.POST["quantity"]
            image = form.cleaned_data['image']
            # fs = FileSystemStorage()
            # fs.save(image.name, image)                                 #сохранение image на сервер
            if "image" in request.FILES:
                product.image_product = request.FILES["image"]  # запись Image в переменную БД
            product.save()
            logger.info(f"Product {product.name_product} is changed successfully")
            return redirect("product", id_product=product.id)
    else:
        form = ProductForm()

    context = {
        "form": form,
        "product": product,
    }
    return render(request, "dzapp/product_form.html", context=context)


# форма для выбора  продукции по id для формы редактирования продукта
def choice_product_by_id(request):
    if request.method == "POST":
        form = ChoiceProductById(request.POST, request.FILES)
        if form.is_valid():
            id_product = request.POST['id_product']

            return redirect("product_form", id_product)
    else:
        form = ChoiceProductById()

    context = {
        "form": form
    }
    return render(request, "dzapp/choice_product_form.html", context=context)


#форма для выбора клиента и кол дней
def choice_products_by_client_by_days(request):
    if request.method == "POST":
        form = ChoiceProductByClientBydays(request.POST, request.FILES)
        if form.is_valid():
            id_client = request.POST['id_client']
            days = request.POST['days']

            return redirect("client_products_sorted", id_client, days)
    else:
        form = ChoiceProductByClientBydays()

    context = {
        "form": form
    }
    return render(request, "dzapp/choice_product_days_form.html", context=context)


def choice_product(request):
    if request.method == "POST":
        form = ChoiceProductById(request.POST, request.FILES)
        if form.is_valid():
            id_product = request.POST['id_product']

            return redirect("product", id_product)
    else:
        form = ChoiceProductById()

    context = {
        "form": form
    }
    return render(request, "dzapp/choice_product_form.html", context=context)
