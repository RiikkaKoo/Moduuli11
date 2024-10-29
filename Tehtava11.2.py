# Kirjoita aiemmin laatimallesi Auto-luokalle aliluokat Sähköauto ja Polttomoottoriauto.
# Sähköautolla on ominaisuutena akkukapasiteetti kilowattitunteina. Polttomoottoriauton
# ominaisuutena on bensatankin koko litroina. Kirjoita aliluokille alustajat. Esimerkiksi
# sähköauton alustaja saa parametreinaan rekisteritunnuksen, huippunopeuden ja akkukapasiteetin.
# Se kutsuu yliluokan alustajaa kahden ensin mainitun asettamiseksi sekä asettaa oman kapasiteettinsa.
# Kirjoita pääohjelma, jossa luot yhden sähköauton (ABC-15, 180 km/h, 52.5 kWh) ja
# yhden polttomoottoriauton (ACD-123, 165 km/h, 32.3 l). Aseta kummallekin autolle haluamasi nopeus,
# käske autoja ajamaan kolmen tunnin verran ja tulosta autojen matkamittarilukemat.

class Auto:
    def __init__(self, rekisteritunnus, huippunopeus, t_nopeus = 0, matka = 0):
        self.rekisteritunnus = rekisteritunnus
        self.huippunopeus = huippunopeus
        self.tamanhetkinen_nopeus = t_nopeus
        self.kuljettu_matka = matka

    # Lisää tai vähentää nopeutta annetulla muutoksella kunnes kohdataan min(0) tai max(huippunopeus) nopeus:
    def kiihdytä(self, nopeuden_muutos):
        if nopeuden_muutos < 0:
            toistot = nopeuden_muutos * -1
        else:
            toistot = nopeuden_muutos
        for i in range(toistot):
            if self.tamanhetkinen_nopeus < self.huippunopeus and nopeuden_muutos >= 0:
                self.tamanhetkinen_nopeus = self.tamanhetkinen_nopeus + 1
            elif nopeuden_muutos < 0 and self.tamanhetkinen_nopeus > 0:
                self.tamanhetkinen_nopeus = self.tamanhetkinen_nopeus - 1

    def kulje_km(self):
        self.kuljettu_matka = self.kuljettu_matka + 1

    def tulosta_lukemat(self):
        print(f"Rekisteritunnus: {self.rekisteritunnus}\n"
              f"\n"
              f"Ajettu matka: {self.kuljettu_matka} km\n"
              f"Nopeus: {self.tamanhetkinen_nopeus} / {self.huippunopeus} km/h")


class SäAuto(Auto):
    def __init__(self, rekisteritunnus, huippunopeus, akkukapasiteetti):
        super().__init__(rekisteritunnus,huippunopeus)
        self.akkukapasiteetti = akkukapasiteetti
        self.akkua_jäljellä = akkukapasiteetti

    # "Kaikissa ympärivuotisissa olosuhteissa sähköautojen kulutus mahtuu käytännössä välille 15–35 kWh/100 km."
    # (https://www.motiva.fi/ratkaisut/kestava_liikenne_ja_liikkuminen/valitse_auto_viisaasti/ajoneuvotekniikka/moottoritekniikka/sahkoautot)
    # Funktio tyhjentää akkua aina yhden kilometrin aikana käytetyllä kilowattitunnilla:
    def tyhjennä_akkua(self):
        self.akkua_jäljellä = self.akkua_jäljellä - (0.01 * 25) # <--- keskimääräinen kWh/100 km tuon lähteen perusteella
        if self.akkua_jäljellä > 0:
            akku_tyhjä = False
        else:
            akku_tyhjä = True
        return akku_tyhjä

    def tulosta_lukemat(self):
        print("-------------------------------------")
        super().tulosta_lukemat()
        print(f"Akku: {self.akkua_jäljellä} / {self.akkukapasiteetti} kWh")
        print("-------------------------------------")


class PmAuto(Auto):
    def __init__(self, rekisteritunnus, huippunopeus, bensatankki):
        super().__init__(rekisteritunnus, huippunopeus)
        self.bensatankki = bensatankki
        self.bensaa_jäljellä = bensatankki

    # "Dieselauto, jonka kulutus on 5 l/100 km, tarvitsee energiaa noin 50 kWh/100 km ja 8 l/100 km kuluttava
    # bensiiniauto noin 72 kWh/100 km."
    # (https://www.motiva.fi/ratkaisut/kestava_liikenne_ja_liikkuminen/valitse_auto_viisaasti/ajoneuvotekniikka/moottoritekniikka/sahkoautot)
    # Funktio tyhjentää tankkia aina yhden kilometrin aikana käytetyllä litramäärällä:
    def käytä_bensaa(self):
        self.bensaa_jäljellä = self.bensaa_jäljellä - (0.01 * 8) # <--- keskimääräinen l/100 km tuon lähteen perusteella
        if self.bensaa_jäljellä > 0:
            tankki_tyhjä = False
        else:
            tankki_tyhjä = True
        return tankki_tyhjä

    def tulosta_lukemat(self):
        print("-------------------------------------")
        super().tulosta_lukemat()
        print(f"Bensatankki: {self.bensaa_jäljellä:.1f} / {self.bensatankki} l")
        print("-------------------------------------")


e_auto = SäAuto("ABC-15", 180, 52.5)
pm_auto = PmAuto("ACD-123", 165, 32.2)

# Ajetaan sähköautoa 60 km/h kolmen tunnin ajan. Kuljettua matka ei kasva, jos akku tyhjenee.
e_auto.tamanhetkinen_nopeus = 60
kilometrit = e_auto.tamanhetkinen_nopeus * 3
akku_tyhjä = False
toistot = 0
while akku_tyhjä == False and toistot != kilometrit:
    akku_tyhjä = e_auto.tyhjennä_akkua()
    #print(e_auto.akkua_jäljellä) # Tarkistaa akun tilanteen muutoksen
    e_auto.kulje_km()
    #print(e_auto.kuljettu_matka) # Tarkistaa kuljetun matkan muutoksen
    toistot += 1
print()

# Ajetaan polttomoottoriautoa 90 km/h kolmen tunnin ajan. Kuljettua matka ei kasva, jos tankki tyhjenee.
pm_auto.tamanhetkinen_nopeus = 90
kilometrit = pm_auto.tamanhetkinen_nopeus * 3
tankki_tyhjä = False
toistot = 0
while tankki_tyhjä == False and toistot != kilometrit:
    tankki_tyhjä = pm_auto.käytä_bensaa()
    #print(pm_auto.bensaa_jäljellä) # Tarkistaa tankin tilanteen muutoksen
    pm_auto.kulje_km()
    #print(pm_auto.kuljettu_matka) # Tarkistaa kuljetun matkan muutoksen
    toistot += 1

print("Autojen mittarilukemat: ")
print()

e_auto.tulosta_lukemat()
print()
pm_auto.tulosta_lukemat()