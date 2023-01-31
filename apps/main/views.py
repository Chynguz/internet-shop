from django.shortcuts import render
from django.http import HttpResponseRedirect
from apps.main.models import Product, Category
# Create your views here.

def main(request):
    product = Product.objects.all()
    category = Category.objects.all()
    return render(request, 'index.html', {'product':product, 'category':category})


def info(request, id):
    info = Product.objects.get(id = id)
    return render(request, 'info.html', {'info':info})

def add_to_cart(request, id):
    cart_session = request.session.get('cart_session1', [])
    cart_session.append(id)
    request.session['cart_session1'] = cart_session
    print(cart_session)
    return HttpResponseRedirect('/')

def cart(request):
    cart_session = request.session.get('cart_session1', [])
    amount = len(cart_session)
    products = Product.objects.filter(id__in = cart_session)
    total_price = 0
    for i in products:
        i.count = cart_session.count(i.id)
        i.sum = i.count * i.price
        total_price += i.sum
    context = {'products':products, 'amount':amount, 'total_price':total_price}
    return render(request, 'cart.html', context)

def remove(request, id):
    cart_session = request.session.get('cart_session1', [])
    g = cart_session
    g.remove(id)
    print(g)
    request.session['cart_session'] = g
    return HttpResponseRedirect('/')
