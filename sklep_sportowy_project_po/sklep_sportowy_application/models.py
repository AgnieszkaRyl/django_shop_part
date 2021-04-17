from django.db import models
from django.urls import reverse
from django.conf import settings

class Adresy(models.Model):
    def __str__(self):
        return self.miasto
    id = models.BigAutoField(primary_key=True)
    ulica = models.CharField(max_length=30)
    kod_pocztowy = models.CharField(max_length=6)
    miasto = models.CharField(max_length=30)


class KartyKlienta(models.Model):
    id = models.BigAutoField(primary_key=True)
    punkty = models.IntegerField()


class Konta(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,) #one user can only have one customer
    id_adresy = models.ForeignKey(Adresy, models.DO_NOTHING, db_column='id_adresy') #jak mamy one to one to w nawiasach dajemy do czego
    id_karta_klienta = models.ForeignKey(KartyKlienta, models.DO_NOTHING, db_column='id_karta_klienta')


class KontaPracownicze(models.Model):
    id = models.BigAutoField(primary_key=True)
    login = models.CharField(max_length=255)
    hasło = models.CharField(max_length=255)
    imie = models.CharField(db_column='Imie', max_length=255)  # Field name made lowercase.
    nazwisko = models.CharField(db_column='Nazwisko', max_length=255)  # Field name made lowercase.



class Newsletter(models.Model):
    email = models.CharField(unique=True, max_length=30)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = True

class Znizki(models.Model):
    id = models.BigAutoField(primary_key=True)
    czy_procentowa = models.IntegerField()
    wartosc = models.FloatField()

class Produkty(models.Model):
    id = models.BigAutoField(primary_key=True)
    nazwa = models.CharField(max_length=30)
    typ = models.CharField(max_length=30)
    cena = models.FloatField()
    dla_kogo = models.CharField(max_length=1)
    id_znizka = models.ForeignKey('Znizki', models.DO_NOTHING, db_column='id_znizka', blank=True, null=True)
    liczba_dostepnych = models.IntegerField()
    #img_path = models.CharField(max_length=255, default=None, blank=True, null=True)
    image=models.ImageField(null=True, blank=True)
    czy_dostepny = models.BooleanField(default=True)

    def __str__(self):
        return self.nazwa

    @property
    def get_available(self):
        return Produkty.objects.filter(czy_dostepny=True)

    def get_id_product_added(self):
        return self.id

    def get_absolute_url(self):
        return reverse('sklep_sportowy:product_details',args=[self.id])

    def get_reclamation_id(self):
        return reverse('sklep_sportowy:reclamation',args=[self.id])

class Reklamacje(models.Model):
    ROZWIAZANIA = [('ZW','Zwrot za gotówke'),('W','Wymiana na nowy'),('N','Naprawa')]
    id = models.BigAutoField(primary_key=True)
    data_reklamacji = models.DateField(auto_now_add=True, blank=True)
    status = models.CharField(max_length=30)
    id_podukt = models.ForeignKey(Produkty, models.DO_NOTHING, db_column='id_podukt')
    kontaid = models.ForeignKey(Konta, models.DO_NOTHING, db_column='Kontaid')  # Field name made lowercase.
    adres = models.ForeignKey(Adresy, models.DO_NOTHING)
    powod_reklamacji = models.CharField(max_length=255)
    preferowane_rozwiazanie = models.CharField(max_length=30, choices=ROZWIAZANIA)
    class Meta:
        managed = True

class Zamowienia(models.Model):
    id = models.BigAutoField(primary_key=True)
    cena_suma = models.FloatField()
    status = models.CharField(max_length=30)
    id_adres = models.ForeignKey(Adresy, models.DO_NOTHING, db_column='id_adres')
    data_zamowienia = models.DateField()
    id_konto = models.ForeignKey(Konta, models.DO_NOTHING, db_column='id_konto', blank=True, null=True)
    czy_oplacony=models.BooleanField(default=False)

    @property
    def get_cart_items(self):
        zamowieniaprodukty=self.zamowieniaprodukty_set.all() #bo zamowieniaprodukty to dziecko
        return sum([item.licznosc for item in zamowieniaprodukty])

    @property
    def get_cart_total(self):
        zamowieniaprodukty = self.zamowieniaprodukty_set.all()
        total=sum([item.get_total for item in zamowieniaprodukty])
        return total

class ZamowieniaProdukty(models.Model):
    zamowieniaid = models.ForeignKey(Zamowienia, models.DO_NOTHING, db_column='Zamowieniaid')  # Field name made lowercase.
    produktyid = models.ForeignKey(Produkty, models.DO_NOTHING, db_column='Produktyid')  # Field name made lowercase.
    licznosc = models.IntegerField()

    @property
    def get_total(self):
        return self.produktyid.cena*self.licznosc


