import requests
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required

from .models import *


@login_required
def Home(request):
    cats = Categories.objects.all()
    bans = Banners.objects.all()

    context = {
        'categories': cats,
        'banners': bans,
    }

    return render(request, 'home.html', context)


@login_required
def AboutUs(request):
    return render(request, 'about.html')


@login_required
def Category(request, id):
    products = Products.objects.filter(category_id=id)
    categ = Categories.objects.all()
    context = {
        'products': products,
        'categories': categ
    }
    return render(request, 'shop.html', context)


@login_required
def Blog(request):
    return render(request, 'blog.html')


@login_required
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


@login_required
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
        shop.total += product.discount
    else:
        ShopItems.objects.create(shop=shop, product=product, quantity=1, total=product.price)
        shop.total += product.price
    shop.save()
    return redirect('/')


@login_required
def Cart(request):
    products = ShopItems.objects.filter(shop__client=request.user, shop__status=0)

    context = {
        'products': products
    }
    return render(request, 'cart.html', context)


def DeleteCart(request, id):
    item = ShopItems.objects.get(id=id)
    item.delete()

    return redirect('/cart/')


def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Tizimmuvaffaqiyatli kirdingiz!")
            return redirect('/')
        else:
            messages.error(request, "login yoki parol xato")
            return redirect('/login/')

    return render(request, 'login.html')


def Logout(request):
    logout(request)
    messages.success(request, "Tizimdan chiqish muvaffaqiyatli yakunlandi!")
    return redirect('/login/')


def Register(request):
    if request.method == "POST":
        r = request.POST
        username = r['username']
        password = r['password']
        ism = r['ism']
        fam = r['fam']
        phone = r['phone']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return redirect('/login/')
        else:
            user = User.objects.create(username=username, password=password, first_name=ism, last_name=fam)
            UserPhone.objects.create(user=user, phone=phone)
            login(request, user)
            messages.success(request, "Tizimga muvaffaqiyatli kirdingiz!")
            return redirect('/')

    else:
        return render(request, 'register.html')
