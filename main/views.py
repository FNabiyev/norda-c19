import requests
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from .models import *

def Home(request):
    cats = Categories.objects.all()
    bans = Banners.objects.all()

    context = {
        'categories':cats,
        'banners':bans,
    }

    return render(request, 'home.html', context)


def AboutUs(request):

    return render(request, 'about.html')


def Category(request, id):
    products = Products.objects.filter(category_id=id)
    categ = Categories.objects.all()
    context = {
        'products':products,
        'categories':categ
    }
    return render(request, 'shop.html', context)


def Blog(request):
    return render(request, 'blog.html')

def Contact(request):
    return render(request, 'contact.html')

def SendMsg(request):

    name = request.POST['name']
    email = request.POST['email']
    subject = request.POST['subject']
    message = request.POST['message']

    bot_token = '1982165731:AAEdCbZ5ev5JoMkL8nv2Po_8AoCw-miK9Ss'
    text = 'Saytdan xabar:\n\nIsmi : ' + name + '\nemail : ' + email + '\nkasbi : ' + subject + '\nxabar : ' + message
    url = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id='
    requests.get(url + '734048744' + '&text=' + text)

    return redirect('/contact/')


class ProductDetail(DetailView):
    model = Products
    template_name = 'product-details.html'
    context_object_name = 'product'


def AddToCart(request, pk):
    user = request.user
    # 1 - holat
    # shop = Shop.objects.filter(client=user, status=0)
    # if len(shop) == 0:
    #     shop = Shop.objects.create(client=user)
    # else:
    #     shop = Shop.objects.get(client=user, status=0)
    #
    # 2- holat
    try:
        shop = Shop.objects.get(client=user, status=0)
    except:
        shop = Shop.objects.create(client=user)
    product = Products.objects.get(id=pk)
    if product.discount:
        ShopItems.objects.create(shop=shop, product=product, quantity=1, total=product.discount)
        shop.total +=product.discount
    else:
        ShopItems.objects.create(shop=shop, product=product, quantity=1, total=product.price)
        shop.total += product.price
    shop.save()
    return redirect('/')