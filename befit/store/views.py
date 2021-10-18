from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
import re
from django.http import HttpResponse


from .models import *
from .utils import cartData

# Create your views here.

def store(request):

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products1 = Product.objects.filter(category=1)
    products1 = products1[0:4]
    products2 = Product.objects.filter(category=2)
    products2 = products2[0:4]
    products3 = Product.objects.filter(category=3)
    products3 = products3[0:4]

    context = {'products1':products1,"products2": products2,"products3":products3,'cartItems':cartItems}
    return render(request, 'store/store.html', context)


def cart(request):

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
                country=data['shipping']['country'],
            )

    else:
        print('User is not logged in')
    return JsonResponse('Payment done', safe=False)





def dashboard_view(request):
    return render(request,"dashboard.html",{})


def search_view(request,*args,**kwargs):
        l= set()
        products = Product.objects.all()
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
        search_list= list()
        search= request.POST.get("search")
        print(search,type(search))
        # print(products)
        if " " in search:
            search_list= search.split(" ")
        else:
            search_list.append(search)
        l_products= list(products)
        # l_product= map(lambda x: str(x),l_products)
        for j in search_list:
            for product in l_products:
                print(product)
                p= str(product)
                if " " in p:
                    p= p.split(" ")
                    for i in p:
                        if re.match(j,i,flags=re.IGNORECASE):
                            l.add(product)
                else:
                    if re.match(j,str(product),flags=re.IGNORECASE):
                        l.add(product)
                # return render(request,"filter.html",{})
        number= len(l)    
        return render(request,"filter.html",{"products":l,"search":search,"n":number,'cartItems':cartItems})


