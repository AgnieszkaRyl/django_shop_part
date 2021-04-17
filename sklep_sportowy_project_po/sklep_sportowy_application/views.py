from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render,HttpResponseRedirect, redirect, get_object_or_404

from .models import  *
from django.http import JsonResponse, HttpRequest
from django.urls import reverse
import json
from django.contrib import messages
import time
from datetime import date


def store(request):
    products=Produkty.objects.filter(czy_dostepny=True)
    context={'products':products}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        id_konto_logged=request.user.id
        print("typ tp: ",type(id_konto_logged))
        konto = Konta.objects.get(id=id_konto_logged)
        adres = Adresy.objects.get(id=1)
        order, created=Zamowienia.objects.get_or_create(id_konto=konto, czy_oplacony=False, defaults={'cena_suma':0, 'status':"gotowy", 'id_adres':adres, 'data_zamowienia':date.today()})
        items=order.zamowieniaprodukty_set.all()    #przeszukujemy dziedzi order
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0}
    context={'items':items, 'order':order}
    return render(request, 'store/cart.html', context)


def add_to_cart(request, id):
    item = get_object_or_404(Produkty, id=id)
    id_konto_logged = request.user.id
    adres=Adresy.objects.get(id=1)
    konto = Konta.objects.get(id=id_konto_logged)
    cart, created=Zamowienia.objects.get_or_create(id_konto=konto, czy_oplacony=False, defaults={'cena_suma':0, 'status':"gotowy", 'id_adres':adres, 'data_zamowienia':date.today(), 'czy_oplacony':False}) #from datetime import date
    orderProducts, created=ZamowieniaProdukty.objects.get_or_create(zamowieniaid=cart, produktyid=item, defaults={'licznosc':0})
    if item.liczba_dostepnych == 0:
        messages.error(request, "Ten produkt jest już niedostępny ")
    else:
        if item.liczba_dostepnych == 1:
            item.czy_dostepny=False
        orderProducts.licznosc+=1
        cart.cena_suma+=item.cena
        item.liczba_dostepnych-=1
        item.save()
        orderProducts.save()
        cart.save()
    return redirect('cart')

def add_to_cart_from_store(request, id):
    item = get_object_or_404(Produkty, id=id)
    id_konto_logged = request.user.id
    adres=Adresy.objects.get(id=1)
    konto = Konta.objects.get(id=id_konto_logged)
    cart, created=Zamowienia.objects.get_or_create(id_konto=konto, czy_oplacony=False, defaults={'cena_suma':0, 'status':"gotowy", 'id_adres':adres, 'data_zamowienia':date.today(), 'czy_oplacony':False}) #from datetime import date
    orderProducts, created=ZamowieniaProdukty.objects.get_or_create(zamowieniaid=cart, produktyid=item, defaults={'licznosc':0})

    if item.liczba_dostepnych == 1:
        item.czy_dostepny = False
    orderProducts.licznosc+=1
    item.liczba_dostepnych-=1
    cart.cena_suma+=item.cena
    item.save()
    orderProducts.save()
    cart.save()
    return redirect('store')

def deleteFromCart(request,id):
    item =get_object_or_404(Produkty, id=id)
    id_konto_logged=request.user.id
    konto=Konta.objects.get(id=id_konto_logged)
    cart = Zamowienia.objects.get(id_konto=konto, czy_oplacony=False)
    orderProducts = ZamowieniaProdukty.objects.get(produktyid=item, zamowieniaid=cart.id)
    if orderProducts.licznosc==1:
        orderProducts.delete()  #usuwamy calkiem z koszyka jesli tylko jeden produkt był
        cart.cena_suma-=item.cena
        item.liczba_dostepnych+=1
        item.czy_dostepny=True
        item.save()
        cart.save()
    else:
        orderProducts.licznosc-=1
        cart.cena_suma-=item.cena
        item.liczba_dostepnych += 1
        item.czy_dostepny=True
        item.save()
        orderProducts.save()
        cart.save()
    #cart.save()
    return redirect('cart')

def login_view(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        print(request.POST)
        if form.is_valid():
            #form.save()
            user=form.get_user()
            print(user)
            login(request, user)
            return redirect('store')
    else:
        form=AuthenticationForm()
    return render(request, 'store/login.html', {'form':form})

def payment_option(request):
    return render(request, 'store/paymentoption.html')

def blik_option(request):
    return render(request, 'store/blik.html')

def credit_card_option(request):
    return render(request, 'store/creditcard.html')

def payment_transfer_option(request):
    return render(request, 'store/paymentransfer.html')

def payment_menage(request):
    id_konto_logged = request.user.id
    print(id_konto_logged)
    zamowienie = Zamowienia.objects.get(id_konto=id_konto_logged, czy_oplacony=False)
    print(zamowienie.id_konto)
    zamowienie.czy_oplacony=True
    zamowienie.save()
    return redirect('store')










def checkout(request):
    if request.user.is_authenticated:
        id_konto_logged = request.user.id  # to jest user admin ma tylko username i password
        order, created = Zamowienia.objects.get_or_create(id_konto=id_konto_logged)
        items = order.zamowieniaprodukty_set.all()  # przeszukujemy dziedzi order
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)


