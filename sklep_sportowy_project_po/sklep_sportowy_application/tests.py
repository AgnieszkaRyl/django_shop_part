from django.test import TestCase
from .models import *
from .views import *
from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date

# Create your tests here.

class ZamowieniaProduktyTestItems(TestCase):
    #@classmethod
    def setUp(self):
        firstProduct=Produkty.objects.create(nazwa='piłka tenisowa', typ='piłka', cena=3.0, dla_kogo='K', liczba_dostepnych=3, czy_dostepny=True)
        secondProduct=Produkty.objects.create(nazwa='buty sportowe', typ='buty', cena=5.0, dla_kogo='M', liczba_dostepnych=3, czy_dostepny=True)
        thirdProduct=Produkty.objects.create(nazwa='buty gorskie', typ='kurtka', cena=5.0, dla_kogo='M', liczba_dostepnych=3, czy_dostepny=True)
        adres=Adresy.objects.create(ulica="wyszynska", kod_pocztowy="66988", miasto="wroclaw")
        konto=Konta.objects.create(user=User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword'),id_adresy=adres,
                                   id_karta_klienta=KartyKlienta.objects.create(punkty=0))
        zamowienie=Zamowienia.objects.create(cena_suma=3.0, status='nadano',id_adres=adres,
                                  data_zamowienia = date.today(), id_konto =konto, czy_oplacony=False)
        ZamowieniaProdukty.objects.create(zamowieniaid=zamowienie, produktyid=firstProduct, licznosc=1 )
        ZamowieniaProdukty.objects.create(zamowieniaid=zamowienie, produktyid=secondProduct, licznosc=5 )
        ZamowieniaProdukty.objects.create(zamowieniaid=zamowienie, produktyid=thirdProduct, licznosc=0 )

    def testGetTotalForOne(self):
        zamowieniAProdukty = ZamowieniaProdukty.objects.all()[0]
        total = zamowieniAProdukty.get_total
        self.assertEqual(total, 3.0)

    def testGetTotalForMany(self):
        zamowieniAProdukty = ZamowieniaProdukty.objects.all()[1]
        total = zamowieniAProdukty.get_total
        self.assertEqual(total, 25.0)


    def testGetTotalForZero(self):
        zamowieniAProdukty = ZamowieniaProdukty.objects.all()[2]
        total = zamowieniAProdukty.get_total
        self.assertEqual(total, 0)


class ZamowieniaTestItems(TestCase):
    def setUp(self):
        firstProduct=Produkty.objects.create(nazwa='kurtka', typ='piłka', cena=3.0, dla_kogo='K', liczba_dostepnych=3, czy_dostepny=True)
        secondProduct=Produkty.objects.create(nazwa='buty gorskie', typ='buty', cena=5.0, dla_kogo='M', liczba_dostepnych=3, czy_dostepny=True)
        adres=Adresy.objects.create(ulica="wyszynska", kod_pocztowy="66988", miasto="wroclaw")
        konto=Konta.objects.create(user=User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword'),id_adresy=adres,id_karta_klienta=KartyKlienta.objects.create(punkty=0))
        zamowienie=Zamowienia.objects.create(cena_suma=3.0, status='nadano',id_adres=adres,
                                  data_zamowienia = date.today(), id_konto =konto, czy_oplacony=False)
        zamowienieSecond = Zamowienia.objects.create(cena_suma=3.0, status='nadano', id_adres=adres,
                                               data_zamowienia=date.today(), id_konto=konto, czy_oplacony=False)
        zamowienieThird = Zamowienia.objects.create(cena_suma=3.0, status='nadano', id_adres=adres,
                                                     data_zamowienia=date.today(), id_konto=konto, czy_oplacony=False)
        ZamowieniaProdukty.objects.create(zamowieniaid=zamowienie, produktyid=firstProduct, licznosc=1 )
        ZamowieniaProdukty.objects.create(zamowieniaid=zamowienieSecond, produktyid=secondProduct, licznosc=5 )
        ZamowieniaProdukty.objects.create(zamowieniaid=zamowienieThird, produktyid=secondProduct, licznosc=5 )
        ZamowieniaProdukty.objects.create(zamowieniaid=zamowienieThird, produktyid=firstProduct, licznosc=5 )

    def testGetItemsAmountForOne(self):
        zamowienia=Zamowienia.objects.all()[0]
        cartItems=zamowienia.get_cart_items

        self.assertEqual(cartItems, 1)

    def testGetItemsAmountForManyOneType(self):
        zamowienia=Zamowienia.objects.all()[1]
        cartItems=zamowienia.get_cart_items

        self.assertEqual(cartItems, 5)

    def testGetItemsAmountForManyDifferentTypes(self):
        zamowienia=Zamowienia.objects.all()[2]
        cartItems=zamowienia.get_cart_items

        self.assertEqual(cartItems, 10)

    def testGetItemsTotalForOne(self):
        zamowienia=Zamowienia.objects.all()[0]
        cartItems=zamowienia.get_cart_total

        self.assertEqual(cartItems, 3.0)

    def testGetItemsTotalForManyOneType(self):
        zamowienia=Zamowienia.objects.all()[1]
        cartItems=zamowienia.get_cart_total

        self.assertEqual(cartItems, 25.0)

    def testGetItemsTotalForManyDifferentTypes(self):
        zamowienia=Zamowienia.objects.all()[2]
        cartItems=zamowienia.get_cart_total

        self.assertEqual(cartItems, 40.0)

class FilterTest(TestCase):
    def setUp(self):
        Produkty.objects.create(nazwa='piłka do siatkowki', typ='piłka', cena=3.0, dla_kogo='K', liczba_dostepnych=3, czy_dostepny=True)
        Produkty.objects.create(nazwa='buty gorskie', typ='buty', cena=3.0, dla_kogo='M', liczba_dostepnych=3, czy_dostepny=True)
        Produkty.objects.create(nazwa='buty sportowe', typ='buty', cena=3.0, dla_kogo='D', liczba_dostepnych=3, czy_dostepny=True)
        Produkty.objects.create(nazwa='piłka futbolowa', typ='piłka', cena=3.0, dla_kogo='U', liczba_dostepnych=0, czy_dostepny=False)

    def test_fiter_available(self):
        products=Produkty.objects.all()[0]
        avaliable=products.get_available
        self.assertEqual(len(avaliable), 3)