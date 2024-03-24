from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from . utils import cookieCart, cartData, guestOrder
from django.views.generic import DeleteView
from django.core.paginator import Paginator


from .models import *

from django.db.models import Q
from django.db.models.functions import Lower, Trim


Praginator_number = 15


def search(request):
    query = request.GET.get('query')
    if query:
        # query1 = query
        # search by name or part number, ignoring case
        query = query.lower()
        # products = Product.objects.annotate(
        #     lower_stripped_name=Lower('name'),
        #     lower_part_number=Lower('part_number')
        # ).filter(Q(lower_stripped_name__icontains=query) | Q(lower_part_number__icontains=query) | Q(
        #     name__icontains=query1) | Q(part_number__icontains=query1))
        products = Product.objects.annotate(
            lower_stripped_name=Lower('name'),
            lower_part_number=Lower('part_number')
        ).filter(Q(lower_stripped_name__icontains=query) | Q(lower_part_number__icontains=query))
    else:
        # show all products
        products = Product.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
    paginator = Paginator(products, Praginator_number)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


# Create your views here.
def index(request):
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems': cartItems}
    return render(request, 'store/index.html', context)


def store(request):

    # data = cartData(request)
    # cartItems = data['cartItems']
    #
    # products = Product.objects.all()
    # context = {'products': products, 'cartItems': cartItems}
    # return render(request, 'store/store.html', context)

    # data = cartData(request)
    # cartItems = data['cartItems']
    #
    # products = Product.objects.all()
    # paginator = Paginator(products, 9)  # Show count products per page
    #
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    #
    # context = {'page_obj': page_obj, 'cartItems': cartItems}
    # return render(request, 'store/store.html', context)

    data = cartData(request)
    cartItems = data['cartItems']

    # Get all the categories for the filter
    categories = CategoryProduct.objects.all()

    # Get the selected category from the request GET parameters
    category_id = request.GET.get('category')

    # If the user has selected a category, filter the products by that category
    if category_id:
        products = CategoryProduct.objects.get(id=category_id).products.all()
    else:
        products = Product.objects.all()

    # Pagination code
    paginator = Paginator(products, Praginator_number)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'cartItems': cartItems, 'categories': categories,
               'selected_category': category_id}
    return render(request, 'store/store.html', context)


def privacy(request):

    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems': cartItems}
    return render(request, 'store/privacy.html', context)


def checkoutthx(request):

    data = cartData(request)
    cartItems = data['cartItems']


    context = {'cartItems': cartItems}
    return render(request, 'store/checkoutthx.html', context)


def about(request):

    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems': cartItems}
    return render(request, 'store/about.html', context)


def contacts(request):

    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems': cartItems}
    return render(request, 'store/contacts.html', context)


class ItemsDetailView(DeleteView):
    model = Product
    template_name = 'store/item.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        data = cartData(self.request)
        cartItems = data['cartItems']

        context['cartItems'] = cartItems
        return context


def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    # print('orderSend:', order, 'itemsSend:', items)

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    # print('Action:', action)
    # print('ProductId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    ordeerItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        ordeerItem.quantity = (ordeerItem.quantity + 1)
    elif action == 'remove':
        ordeerItem.quantity = (ordeerItem.quantity - 1)
    elif action == 'remove-all':
        ordeerItem.quantity = 0

    ordeerItem.save()

    if ordeerItem.quantity <= 0:
        ordeerItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)


    total = float((data['form']['total']).replace(',', '.'))
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            address=data['shipping']['address'],
        )

    return JsonResponse('Payment complete', safe=False)


def handle404(request, exception):
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems': cartItems}
    return render(request, 'store/404.html', context)

