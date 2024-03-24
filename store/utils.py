import json
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from tabulate import tabulate


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    # print('Cart: ', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
    # print('User is not logged in!!!')

    # print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    phone = data['form']['phone']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
        phone=phone,
    )

    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )

    if request.method == 'POST':
        nameq = name
        emailq = email
        phoneq = phone
        addressq = data['shipping']['address']
        cityq = data['shipping']['city']
        stateq = data['shipping']['state']
        itemall = []
        for itemsq in items:
            nameprod = itemsq['product']['name']
            quantityprod = itemsq['quantity']
            priceprod = itemsq['get_total']
            itemall.append({
                'name': nameprod,
                'quantity': quantityprod,
                'price': priceprod
            })


        # send_mail(
        #     'Новый заказ',
        #     "Имя: %s" % nameq + "\n" + "Почта: %s" % emailq + "\n" + "Телефон: %s" % phoneq
        #     + "\n" + "Регион: %s" % cityq + "\n" + "Город: %s" % stateq + "\n" + "Адрес: %s" % addressq
        #     + "\n\n" + "Товары: %s" % itemall,
        #     settings.EMAIL_HOST_USER,
        #     [settings.EMAIL_HOST_USER],
        #     fail_silently=False
        # )
        try:
            sum_table = 0
            table = []
            for item in itemall:
                sum_table += float(item['price'])
                table.append([item['name'], item['quantity'], '{:.2f}'.format(float(item['price']))])

            table.append(['', 'Итого:', '{:.2f}'.format(sum_table)])

            table_headers = ["Товар", "Количество", "Цена"]
            table_str = tabulate(table, headers=table_headers, tablefmt="html", floatfmt=".2f")

            client_data = [['Имя:', nameq], ['Email:', emailq], ['Телефон:', phoneq]]
            client_address = [['Адрес:', addressq], ['Регион:', cityq], ['Город:', stateq]]

            client_data_table = tabulate(client_data, tablefmt="html")
            client_address_table = tabulate(client_address, tablefmt="html")

            body = f"""\
            <html>
                <body>
                    <h2 style='background-color: #e5e7eb; font-weight: bold; font-size: 20px;'>Заказ № {str(order)}</h2>
                    <h2 style='background-color: #F5DEB3;'>Данные клиента:</h2>
                    <span style='font-size: 18px;'>{client_data_table}</span>
                    <h2 style='background-color: #F5DEB3;'>Адрес клиента:</h2>
                    <span style='font-size: 18px;'>{client_address_table}</span>
                    <h2 style='background-color: #F5DEB3;'>Детали заказа:</h2>
                    <span style='font-size: 18px;'>{table_str}</span>
                </body>
            </html>
            """

            send_mail(
                'Новый заказ № %s' % str(order),
                body,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
                html_message=body
            )
        except:
            print("error vpnSmptServer")
            pass


    return customer, order