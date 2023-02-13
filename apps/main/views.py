from django.shortcuts import render
from django.http import HttpResponseRedirect
from apps.main.models import Product, Category
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from django.views.decorators.cache import cache_page
from django.core.cache import cache


# Create your views here.



class MainListView(ListView):
    model = Product
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(MainListView, self).get_context_data(**kwargs)
        cache_category = cache.get('category')
        if not cache_category:
            category = Category.objects.all()
            cache.set('category', category, 10)
        else:
            category = cache_category
        cache_product = cache.get('product')
        if not cache_product:
            product = Product.objects.all()
            cache.set('product', product, 20)
        else:
            product = cache_product
        context['category'] = category
        context['product'] = product
        return context


class AboutUsView(TemplateView):
    template_name = 'about.html'


# class AddtoCard(TemplateView):
#     template_name = HttpResponseRedirect('/')

#     def get_context_data(self, **kwargs):
#         context = super(AddtoCard, self).get_context_data(**kwargs)
#         cart_session = self.request.session.get('cart_session1', [])
#         cart_session.append(self.kwargs['id'])
#         self.request.session['cart_session1'] = cart_session
#         context['cart_session1'] = cart_session
#         return context
    
    

@login_required(login_url='login')
def add_to_cart(request, id):
    cart_session = request.session.get('cart_session1', [])
    cart_session.append(id)
    request.session['cart_session1'] = cart_session
    print(cart_session)
    return HttpResponseRedirect('/')


class CardView(TemplateView):
    template_name = 'cart.html'
        
    def get_context_data(self, **kwargs):
        context = super(CardView, self).get_context_data(**kwargs)
        cart_session = self.request.session.get('cart_session1', [])
        amount = len(cart_session)
        products = Product.objects.filter(id__in = cart_session)
        total_price = 0
        for i in products:
            i.count = cart_session.count(i.id)
            i.sum = i.count * i.price
            total_price += i.sum
        context['products'] = products
        context['amount'] = amount
        context['total_price'] = total_price
        return context



# @login_required(login_url='login')
# def cart(request):
#     cart_session = request.session.get('cart_session1', [])
#     amount = len(cart_session)
#     products = Product.objects.filter(id__in = cart_session)
#     total_price = 0
#     for i in products:
#         i.count = cart_session.count(i.id)
#         i.sum = i.count * i.price
#         total_price += i.sum
#     context = {'products':products, 'amount':amount, 'total_price':total_price}
#     return render(request, 'cart.html', context)

# def orders(request):
#     if request.method == 'POST': 
#         order_session = request.session.get('cart_session1', [])
#         first_name = request.POST.get('ferst_name')
#         last_name = request.POST.get('last_name')
#         address = request.POST.get('address')
#         productes = Product.objects.filter(id__in=order_session)
#         amount = len(order_session)
#         total_price = 0
#         for i in productes:
#             i.count = order_session.count(i.id)
#             i.sum = i.cout * i.price
#             total_price += i.sum
#         context = {'first_name': first_name, 'last_name': last_name, 'address': address, 'amount': amount, 'total_prise': total_price}
#         return render(request, 'order.html', context)


        
class InfoView(TemplateView):
    template_name = 'info.html'

    def get_context_data(self, **kwargs):
        context = super(InfoView, self).get_context_data(**kwargs)
        info = Product.objects.get(id = self.kwargs['id'])
        context['info'] = info
        return context

# def info(request, id):
#     info = Product.objects.get(id = id)
#     return render(request, 'info.html', {'info':info})


# class RemoveView(TemplateView):
#     template_name = 'cart.html'

#     def get_context_data(self, **kwargs):
#         context = super(RemoveView, self).get_context_data(**kwargs)
#         cart_session = self.request.session.get('cart_session1', [])
#         g = cart_session
#         g.remove(self.kwargs['id'])
#         print(g)
#         self.request.session['cart_session1'] = g
#         context['cart_session1'] = g
#         return context


@cache_page(100)
def remove(request, id):
    cart_session = request.session.get('cart_session1', [])
    g = cart_session
    g.remove(id)
    print(g)
    request.session['cart_session'] = g
    return HttpResponseRedirect('/cart')

@cache_page(100)
def search(request):
    if request.method == 'POST':
        product = request.POST.get('product')
        product_model = Product.objects.filter(title = product)
        return render(request, 'search.html', {'product': product_model})

# class SearchView(ListView):
#     template_name = 'search.html'
#     context_object_name = 'product'
#     paginate_by = 5

#     def get_queryset(self):
#         return Product.objects.POST.get(title__icontains=self.request.POST.get('product'))

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['product'] = self.request.POST.get('product')
#         return context

# def category(request, slug):
#     cat = Category.objects.all()
#     category = Category.objects.get(slug = slug)
#     product = Product.objects.filter(category = category)
#     return render(request, 'category.html', {'products': product, 'category': category,'cat':cat})


class CategoryView(ListView):
    model = Category
    template_name = 'category.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        cat = Category.objects.all()
        category = Category.objects.get(slug = self.kwargs['slug'])
        product = Product.objects.filter(category = category)
        context['cat'] = cat
        context['products'] = product
        context['category'] = category
        return context