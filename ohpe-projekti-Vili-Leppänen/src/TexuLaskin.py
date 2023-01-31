import random
import itertools
import ast

def luo_pakka() -> list: 
    """
    Luo korttipakan. Kortit tupleina muodossa esim: [(5,"♥"), (6,"♥"), (14,"♠")]
    """
    funktiopakka = []
    maalista  =["♥","♠","♦","♣"]
    index = 0
    arvo = 2

    for i in range(52):

        funktiopakka.append((arvo, maalista[index]))
        
        arvo += 1
        if arvo > 14:
            arvo -= 13
            index += 1
    
    return funktiopakka

def tunnista_texu(seitsemankorttia: list) -> list:
    """
    Käsientunnistuksen pääfunktio. Testaa kaikki 21 viiden kortin yhdistelmää "main_tunnistus" funktiolla, ja valitsee niistä parhaan palautettavaksi.
    Palauttaa listan jossa paras 5 kortin käsi, käsityypin (esim pari tai suora) kertovan numeron, 
    sekä arvotusnumeron jota voidaan vertailla muiden pelaajien käsiin parhaan käden määrittämiseksi.
    """
    viiden_listat = [] 				#funktion sisäinen lista
    loppulista = [] 				#main tunnistuksesta kaikki tähän, sitten sort ja return paras
    
    seitsemankorttia.sort() 		#kaikki 7 korttia järjestykseen
    
    for L in range(5,6):			#kaikki mahdolliset 5 kortin yhdistelmät omina listoina 
        for viidenyhdistelmat in itertools.combinations(seitsemankorttia, L):
            viiden_listat.append(list(viidenyhdistelmat))
    
    for viidenlista in viiden_listat: 
        viidenlista = main_tunnistus(viidenlista)   
        loppulista.append(list(viidenlista))
        
    loppulista.sort(key=lambda a: a[1], reverse = True) 	#sorttaus arvonumeron mukaan
    
    
    return loppulista[0] 			#palautetaan paras käsi, käsityyppi, ja arvotusnumero

def eri_arvoja(kasi: list) -> int:
    """
    Laskee montaako eri numeroista korttia annetuissa 5 kortissa on. Tätä hyödynnetään käden tarkemmassa tunnistamisessa. Palauttaa vain numeron 2-5.
    Vaatii toimiakseen, että annetut kortit ovat suuruusjärjesyksessä.
    """
    oletus = 5
    
    for i in range(len(kasi)-1):
        if kasi[i][0] == kasi[i + 1][0]:
            oletus -= 1
    
    return oletus

def main_tunnistus(kasi: list) -> tuple: 	
    """
    Saa inputtina 5 kortin listan. Tunnistaa sen useita muita funktioita hyödyntäen. 
    palauttaa tuplen, jossa lista 5 kortista, sekä  tuple jossa käsityyppinro, arvotuslista
    esim ([(5,"♦"),(6,"♣"),(9,"♣"),(11,"♦"),(12,"♣")],(5, 1324354))
    """                                   
    eriarvoja = eri_arvoja(kasi)
    kasityyppinro = []

    if eriarvoja == 5:
        
        # HIGH?
        if eriarvoja == 5 and len(kasityyppinro) <= 0:
            kasityyppinro = oli_high(kasi)
            
        # SUORA?    
        if kasi[0][0] == kasi[1][0]-1:
            if kasi[1][0] == kasi[2][0]-1:
                if kasi[2][0] == kasi[3][0]-1:
                    if kasi[3][0] == kasi[4][0]-1 or (kasi[0][0] == 2 and kasi[4][0] == 14):
                        
                        kasityyppinro = oli_suora(kasi)
        # VÄRI?       
        if kasi[0][1] == kasi[1][1]:
            if kasi[1][1] == kasi[2][1]:
                if kasi[2][1] == kasi[3][1]:
                    if kasi[3][1] == kasi[4][1]:
                        
                        kasityyppinro = oli_vari(kasi)
        # VÄRISUORA?
        if kasi[0][1] == kasi[1][1]:
            if kasi[1][1] == kasi[2][1]:
                if kasi[2][1] == kasi[3][1]:
                    if kasi[3][1] == kasi[4][1]:
                        
                        if kasi[0][0] == kasi[1][0]-1:
                            if kasi[1][0] == kasi[2][0]-1:
                                if kasi[2][0] == kasi[3][0]-1:
                                    if kasi[3][0] == kasi[4][0]-1 or (kasi[0][0] == 2 and kasi[4][0] == 14):
                                        
                                        kasityyppinro = oli_varisuora(kasi) 

    #####################
        
    # PARI? 
    elif eriarvoja == 4:
        
        kasityyppinro = oli_pari(kasi)                          
        
    ######################
        
    elif eriarvoja == 3:


        # KOLMOSET?        
        if (kasi[0][0] == kasi[1][0] == kasi[2][0]) or (kasi[1][0] == kasi[2][0] == kasi[3][0]) or (kasi[2][0] == kasi[3][0] == kasi[4][0]): #xxx & y & z   OR   x & yyy & z   OR    x & y & zzz

            kasityyppinro = oli_kolmoset(kasi)   

        # KAKSI PARIA?
        else:  
            parilaskuri = 0
            
            if kasi[0][0] == kasi[1][0]:
                parilaskuri += 1
            if kasi[1][0] == kasi[2][0]:
                parilaskuri += 1
            if kasi[2][0] == kasi[3][0]:
                parilaskuri += 1
            if kasi[3][0] == kasi[4][0]:
                parilaskuri += 1
            
            if parilaskuri == 2:
                kasityyppinro = oli_kaksiparia(kasi)

    #########################

    elif eriarvoja == 2:
            
        # NELOSET?
        if (kasi[0][0] == kasi[1][0] == kasi[2][0] == kasi[3][0]) or (kasi[1][0] == kasi[2][0] == kasi[3][0] == kasi[4][0]):  # xxxx & y    or    x & yyyy

            kasityyppinro = oli_neloset(kasi) 

        # TÄYSKÄSI?
        elif (kasi[0][0] == kasi[1][0] == kasi[2][0]) and (kasi[3][0] == kasi[4][0]) or (kasi[0][0] == kasi[1][0]) and (kasi[2][0] == kasi[3][0] == kasi[4][0]): # xxx & yy    or    xx & yyy
            kasityyppinro = oli_tayskasi(kasi)
            
            kadenarvo = arvotuslista_yhdeksi(kasityyppinro)
            return (kasi, kadenarvo)
    
    kadenarvo = arvotuslista_yhdeksi(kasityyppinro) #####################
    return (kasi, kadenarvo)

def arvotuslista_yhdeksi(lista: list) -> tuple: 
    """
    Saa inputtina 6 pituisen "arvotuslistan" numeroita 0 - 14, muuntaa ne yhdeksi kantaluku 10 numeroksi. Näitä vertailemalla kaikkien käsien paremmuus selvitettävissä.
    """
    try:
        x = lista[0] * (14 ** 5)
        x += lista[1] * (14 ** 4)
        x += lista[2] * (14 ** 3)
        x += lista[3] * (14 ** 2)
        x += lista[4] * (14 ** 1)
        x += lista[5] * (14 ** 0)
    except:
        print("virhe")                  
        print(f"{hero_kasi}")
        print(f"{lista}")
        return (1, 1)               
    return (x, lista[0])

def oli_high(kasi: list) -> list: 
    """
    luo highn arvotuslistan
    """
    highn_arvolista = []
    highn_arvolista.append(1)    
    highn_arvolista.append(kasi[4][0])
    highn_arvolista.append(kasi[3][0])
    highn_arvolista.append(kasi[2][0])
    highn_arvolista.append(kasi[1][0])
    highn_arvolista.append(kasi[0][0])
    
    return highn_arvolista

def oli_pari(kasi: list) -> list: 
    """
    luo parin arvotuslistan
    """
    parin_arvolista = []
    parin_arvolista.append(2)
    
    if kasi[0][0] == kasi[1][0]:
        
        parin_arvolista.append(kasi[0][0])
        parin_arvolista.append(kasi[4][0])
        parin_arvolista.append(kasi[3][0])
        parin_arvolista.append(kasi[2][0])
        parin_arvolista.append(0)
        
    if kasi[1][0] == kasi[2][0]:
        
        parin_arvolista.append(kasi[1][0])
        parin_arvolista.append(kasi[4][0])
        parin_arvolista.append(kasi[3][0])
        parin_arvolista.append(kasi[0][0])
        parin_arvolista.append(0)
        
    if kasi[2][0] == kasi[3][0]:
        
        parin_arvolista.append(kasi[2][0])
        parin_arvolista.append(kasi[4][0])
        parin_arvolista.append(kasi[1][0])
        parin_arvolista.append(kasi[0][0])
        parin_arvolista.append(0)
        
        
    if kasi[3][0] == kasi[4][0]:
        
        parin_arvolista.append(kasi[3][0])
        parin_arvolista.append(kasi[2][0])
        parin_arvolista.append(kasi[1][0])
        parin_arvolista.append(kasi[0][0])
        parin_arvolista.append(0)

    return parin_arvolista

def oli_kaksiparia(kasi: list) -> list: 
    """
    luo kahden parin arvotuslistan
    """
    kahdenparin_arvolista = []
    kahdenparin_arvolista.append(3)
    
    if kasi[0][0] == kasi[1][0] and kasi[2][0] == kasi[3][0]:
        
        kahdenparin_arvolista.append(kasi[2][0])
        kahdenparin_arvolista.append(kasi[0][0])
        kahdenparin_arvolista.append(kasi[4][0])
        kahdenparin_arvolista.append(0)
        kahdenparin_arvolista.append(0)
        
    if kasi[0][0] == kasi[1][0] and kasi[3][0] == kasi[4][0]:
        
        kahdenparin_arvolista.append(kasi[3][0])
        kahdenparin_arvolista.append(kasi[0][0])
        kahdenparin_arvolista.append(kasi[2][0])
        kahdenparin_arvolista.append(0)
        kahdenparin_arvolista.append(0)

    if kasi[1][0] == kasi[2][0] and kasi[3][0] == kasi[4][0]:
        
        kahdenparin_arvolista.append(kasi[3][0])
        kahdenparin_arvolista.append(kasi[1][0])
        kahdenparin_arvolista.append(kasi[0][0])
        kahdenparin_arvolista.append(0)
        kahdenparin_arvolista.append(0)

    return kahdenparin_arvolista

def oli_kolmoset(kasi: list) -> list: 
    """
    luo kolmosten arvotuslistan
    """
    kolmosten_arvolista = []
    kolmosten_arvolista.append(4)
    
    if kasi[0][0] == kasi[1][0] == kasi[2][0]:
        
        kolmosten_arvolista.append(kasi[0][0])
        kolmosten_arvolista.append(kasi[4][0])
        kolmosten_arvolista.append(kasi[3][0])
        kolmosten_arvolista.append(0)
        kolmosten_arvolista.append(0)
        
    if kasi[1][0] == kasi[2][0] == kasi[3][0]:
        
        kolmosten_arvolista.append(kasi[1][0])
        kolmosten_arvolista.append(kasi[4][0])
        kolmosten_arvolista.append(kasi[0][0])
        kolmosten_arvolista.append(0)
        kolmosten_arvolista.append(0)
    
    if kasi[2][0] == kasi[3][0] == kasi[4][0]:
        
        kolmosten_arvolista.append(kasi[2][0])
        kolmosten_arvolista.append(kasi[1][0])
        kolmosten_arvolista.append(kasi[0][0])
        kolmosten_arvolista.append(0)
        kolmosten_arvolista.append(0)

    return kolmosten_arvolista

def oli_suora(kasi: list) -> list: 
    """
    luo suoran arvotuslistan
    """
    suoran_arvolista = []
    suoran_arvolista.append(5)
    suoran_arvolista.append(kasi[4][0])
    suoran_arvolista.append(kasi[3][0])
    suoran_arvolista.append(kasi[2][0])
    suoran_arvolista.append(kasi[1][0])
    suoran_arvolista.append(kasi[0][0])
    
    if suoran_arvolista[1] == 14 and suoran_arvolista[2] == 5: # jos A - 5, muutetaan listaa
        suoran_arvolista = (5),(5),(4),(3),(2),(1)
        
    return suoran_arvolista

def oli_vari(kasi: list) -> list: 
    """
    luo värin arvotuslistan
    """
    varin_arvolista = []
    varin_arvolista.append(6)    
    varin_arvolista.append(kasi[4][0])
    varin_arvolista.append(kasi[3][0])
    varin_arvolista.append(kasi[2][0])
    varin_arvolista.append(kasi[1][0])
    varin_arvolista.append(kasi[0][0])
    
    return varin_arvolista

def oli_tayskasi(kasi: list) -> list: 
    """
    luo täyskäden arvotuslistan
    """
    tayskaden_arvolista = []
    tayskaden_arvolista.append(7)
    
    if kasi[0][0] == kasi[1][0] == kasi[2][0] and (kasi[3][0] == kasi[4][0]):
        
        tayskaden_arvolista.append(kasi[0][0])
        tayskaden_arvolista.append(kasi[3][0])
        tayskaden_arvolista.append(0)
        tayskaden_arvolista.append(0)
        tayskaden_arvolista.append(0)   
    
    if (kasi[0][0] == kasi[1][0]) and (kasi[2][0] == kasi[3][0] == kasi[4][0]):
        
        tayskaden_arvolista.append(kasi[2][0])
        tayskaden_arvolista.append(kasi[0][0])
        tayskaden_arvolista.append(0)
        tayskaden_arvolista.append(0)
        tayskaden_arvolista.append(0)
    
    return tayskaden_arvolista

def oli_neloset(kasi: list) -> list: 
    """
    luo nelosten arvotuslistan
    """
    nelosten_arvolista = []
    nelosten_arvolista.append(8)
    
    if kasi[0][0] == kasi[1][0] == kasi[2][0] == kasi[3][0]:

        nelosten_arvolista.append(kasi[0][0])
        nelosten_arvolista.append(kasi[4][0])
        nelosten_arvolista.append(0)
        nelosten_arvolista.append(0)
        nelosten_arvolista.append(0)
    
    if (kasi[1][0] == kasi[2][0] == kasi[3][0] == kasi[4][0]):
        
        nelosten_arvolista.append(kasi[1][0])
        nelosten_arvolista.append(kasi[0][0])
        nelosten_arvolista.append(0)
        nelosten_arvolista.append(0)
        nelosten_arvolista.append(0)

    return nelosten_arvolista

def oli_varisuora(kasi: list) -> list: 
    """
    luo värisuoran arvotuslistan
    """
    varisuoran_arvolista = []
    varisuoran_arvolista.append(9)
    varisuoran_arvolista.append(kasi[4][0])
    varisuoran_arvolista.append(kasi[3][0])
    varisuoran_arvolista.append(kasi[2][0])
    varisuoran_arvolista.append(kasi[1][0])
    varisuoran_arvolista.append(kasi[0][0])
    
    if varisuoran_arvolista[1] == 14 and varisuoran_arvolista[2] == 5: # jos A - 5, muutetaan listaa
        varisuoran_arvolista = (1),(5),(4),(3),(2),(1)
        
    return varisuoran_arvolista

def sekoita_pakka(pakka: list) -> list: 
    """
    sekoittaa annetun pakan järjestyksen
    """
    return random.sample(pakka, len(pakka))

def hero_kysely(sekoitettupakka): 
    """
    heron(pelaaja itse) korttien kysely, palauttaa 2 kortin listan
    """
    hyvaksytyt_maat = ["h","s","d","c"]
    maalista  = ["♥","♠","♦","♣"]
    hero_kortit = []
    herokortti1 = None
    herokortti2 = None
    heroarvo1 = None
    heromaa1 = None
    heroarvo2 = None
    heromaa2 = None
    
    
    valmis = False
    while not valmis:

        herokortti1 = input(f"\nAnna ensimmäinen korttisi (arvo = 2 - 14 maa = h/s/d/c, esim: 5 h tai 14 d)\n")

        herokortti2 = input(f"\nAnna toinen korttisi (arvo = 2 - 14 maa = h/s/d/c, esim: 5 h tai 14 d)\n")

        try:
            heroarvo1 = int(herokortti1.split()[0])
            heromaa1 = herokortti1.split()[1]
            heroarvo2 = int(herokortti2.split()[0])
            heromaa2 = herokortti2.split()[1]
        except:
            print("\nYritä uudestaan\n")
            return hero_kysely(sekoitettupakka)
        
        try:
            if heroarvo1 >= 2 and heroarvo1 <= 14 and heroarvo2 >= 2 and heroarvo2 <= 14:
                if heromaa1.lower() in hyvaksytyt_maat and heromaa2.lower() in hyvaksytyt_maat:
                    heromaa1 = maalista[hyvaksytyt_maat.index(heromaa1.lower())]
                    heromaa2 = maalista[hyvaksytyt_maat.index(heromaa2.lower())]

                    hero_kortit =[(int(heroarvo1),str(heromaa1)),(int(heroarvo2),str(heromaa2))]
                    if hero_kortit[0] == hero_kortit[1]:
                        print("\nKorttia ei ole pakassa. Yritä uudestaan.\n")
                        return hero_kysely(sekoitettupakka)
                    
                    else:
                        if hero_kortit[0] in sekoitettupakka and hero_kortit[1] in sekoitettupakka:
                            print(f"\nPelaajalle jaettu {korttientulostus(hero_kortit)}\n")           
                            poista_pakasta(sekoitettupakka, hero_kortit)
                            return hero_kortit, sekoitettupakka
                        else:
                            return hero_kysely(sekoitettupakka)
        except:
            print("\nYritä uudestaan\n")
            return hero_kysely(sekoitettupakka)
        
        print("\nYritä uudestaan\n")
        return hero_kysely(sekoitettupakka)
        
def villain_kysely(sekoitettupakka: list, pelaajanro: int) -> list:
    """
    muiden pelaajien korttien kysely, palauttaa 2 kortin listan
    ottaa inputtina jäljellä olevan korttipakan, sekä pelaajanro:n jota käytetään kortteja käyttäjältä pyytäessä, 
    jotta pysyy kärryillä monellekko pelaajalle kortteja on syötetty.
    """
    hyvaksytyt_maat = ["h","s","d","c"]
    maalista  = ["♥","♠","♦","♣"]
    villain_kortit = []
    villainkortti1 = None
    villainkortti2 = None
    villainarvo1 = None
    villainmaa1 = None
    villainarvo2 = None
    villainmaa2 = None
    
    
    valmis = False
    while not valmis:

        if pelaajanro >= 1:
            villainkortti1 = input(f"\nAnna vastapelaaja {pelaajanro + 1}:n ensimmäinen kortti (arvo = 2 - 14 maa = h/s/d/c) (esim: 5 h tai 14 d):\nJos et halua syöttää enempää vastapelaajia, syötä tyhjä.\n")
        else:
            villainkortti1 = input(f"\nAnna vastapelaaja {pelaajanro + 1}:n ensimmäinen kortti (arvo = 2 - 14 maa = h/s/d/c) (esim: 5 h tai 14 d):\n")

        if villainkortti1 == "":
            return False

        villainkortti2 = input(f"\nAnna vastapelaaja {pelaajanro + 1}:n toinen kortti (arvo = 2 - 14 maa = h/s/d/c) (esim: 5 h tai 14 d):\n")

        try:
            villainarvo1 = int(villainkortti1.split()[0])
            villainmaa1 = villainkortti1.split()[1]
            villainarvo2 = int(villainkortti2.split()[0])
            villainmaa2 = villainkortti2.split()[1]
        except:
            print("\nYritä uudestaan\n")
            return villain_kysely(sekoitettupakka, pelaajanro)
        
        try:
            if villainarvo1 >= 2 and villainarvo1 <= 14 and villainarvo2 >= 2 and villainarvo2 <= 14:
                if villainmaa1.lower() in hyvaksytyt_maat and villainmaa2.lower() in hyvaksytyt_maat:
                    villainmaa1 = maalista[hyvaksytyt_maat.index(villainmaa1.lower())]
                    villainmaa2 = maalista[hyvaksytyt_maat.index(villainmaa2.lower())]

                    villain_kortit =[(int(villainarvo1),str(villainmaa1)),(int(villainarvo2),str(villainmaa2))]
                    if villain_kortit[0] == villain_kortit[1]:
                        print("\nVain yksi pakka käytössä. Yritä uudestaan.\n")
                        return villain_kysely(sekoitettupakka, pelaajanro)
                    
                    else:
                        if villain_kortit[0] in sekoitettupakka and villain_kortit[1] in sekoitettupakka:
                            print(f"\nPelaajalle jaettu {korttientulostus(villain_kortit)}\n")           
                            poista_pakasta(sekoitettupakka, villain_kortit)
                            return villain_kortit, sekoitettupakka
                        else:
                            return villain_kysely(sekoitettupakka, pelaajanro)

        except:
            print("\nYritä uudestaan\n")
            return villain_kysely(sekoitettupakka)
        
        print("\nYritä uudestaan\n")
        return villain_kysely(sekoitettupakka)

def poyta(sekoitettupakka: list) -> list:
    """
    Kyselee käyttäjältä haluaako tämä syöttää pöytäkortteja. Palauttaa listan jossa 0 - 5 korttia
    """
    hyvaksytyt_maat = ["h","s","d","c"]
    maalista  = ["♥","♠","♦","♣"]
    poytakortit = []
    
    poytakysely = input(f"Jos haluat syöttää pöytäkortteja (1 - 5 kpl), syötä ne pilkuilla erotettuna esim: 5 h, 4 d, 12 c.\nJos et halua antaa pöytäkortteja, syötä tyhjä.\n")
    
    if poytakysely == "":
        return ""
    
    kortit = poytakysely.split(",")

    if len(kortit) > 5:
        print("Maksimissaan 5 korttia pöytään")
        return poyta(sekoitettupakka)
    
    else:
        for kortti in kortit:
            try:
                poytaarvo1 = int(kortti.split()[0])
                poytamaa1 = kortti.split()[1]
            except:
                poyta(sekoitettupakka)


                if poytaarvo1 >= 2 and poytaarvo1 <= 14:
                    if poytamaa1.lower() in hyvaksytyt_maat:
                        poytamaa1 = maalista[hyvaksytyt_maat.index(poytamaa1.lower())]
                        lisattavakortti = (int(poytaarvo1),str(poytamaa1))

                        if lisattavakortti in sekoitettupakka and lisattavakortti not in poytakortit:
                            poytakortit.append(lisattavakortti)

    poista_pakasta(sekoitettupakka, poytakortit)
    return poytakortit
    
def poista_pakasta(pakka :list, poistettavat: list) -> list:
    """
    ottaa inputtina jäljellä olevan pakan, sekä sieltä poistettavat kortit. Palauttaa pakan ilman kys kortteja.
    """
    try:
        for kortti in poistettavat:
            pakka.remove(kortti)
    except:
        return None

    return pakka

def eteneminen(tarkkuus: int,testi: int):
    """
    Tarkemmilla tarkkuuksilla kun ohjelmalla kestää hetken laskea, tulostaa käyttäjälle "latauspalkin" jotta tietää että ohjelma etenee kuitenkin.
    Ei palauta mitään.
    """
    if testi == tarkkuus - 1:
        print(f"\nValmis!")

    if tarkkuus == 25000:
        lista = list(range(0,25000,2500))
        if testi in lista:
            print(f"{round(testi / tarkkuus * 100)}% ",end="")
    
    if tarkkuus == 10000:
        lista = list(range(0,10000,1000))
        if testi in lista:
            print(f"{round(testi / tarkkuus * 100)}%  ",end="")

def uudestaan():
    """
    Ohjelman lopetus/kysely, haluaako käyttäjä aloittaa alusta.
    """
    vastaus = input(f"Jos haluat aloittaa alusta, syötä 1, jos haluat lopettaa ohjelman, syötä 0\n")
    if vastaus == "1":
        main()
    if vastaus == "0":
        exit()
        print("yli")
        
    else:
        print(f"Kelvoton vastaus, yritä uudestaan\n")
        uudestaan()

def tulos(kaikkikortit: list, pisteet: list, poyta: list, tarkkuus: int):
    """
    Tulostaa käden tulokset käyttäjän nähtäväksi. Ei palauta mitään
    """
    if len(poyta) > 0:
        print(f"Annetut pöytäkortit: {korttientulostus(poyta)} \n")

    for i in range(len(kaikkikortit)):
        print(f"{korttientulostus(kaikkikortit[i])} Voitto:  {round(pisteet[i][0] / tarkkuus * 100, 2)}%  Split Eq:  {round(pisteet[i][1] / tarkkuus * 100, 2)}%")

    print("")

def testi(hero_kortit: list, villainkortit: list, sekoitettupakka: list, poyta: list, tarkkuus: int):
    """
    Laskinfunktio. Luo listan eri käsien pisteille, pyörittää kädentunnistuksen niin monesti kuin käyttäjä on valinnut (tarkkuus), 
    ja palauttaa pisteet muodossa josta tulos funktio osaa ne tulostaa.
    Palauttaa listan jossa kaikkien pelaajien käsikortit, listan jossa jokaisen pelaajan pisteet samassa järjestyksessä kuin kädet, 
    käyttäjän käteen syöttämät käsikortit, ja käden laskemiseen valitun tarkkuuden.
    """
    testi = 0
    kaikkikortit = [hero_kortit] + villainkortit
    pisteet = []

    for kortit in kaikkikortit:
        pisteet.append([0,0])       #(actual voitot, splitit)

    poytakortit = []

    for kortti in poyta:                #lisätään annetut pöytäkortit, jos on annettu
        poytakortit.append(kortti)
    
    puuttuu = 5 - (len(poytakortit)) 

    while testi < tarkkuus:

        eteneminen(tarkkuus,testi)

        random.shuffle(sekoitettupakka)

        vaihtuvapoyta = poytakortit + sekoitettupakka[0:puuttuu]

        tunnistetutkadet = []

        for kortit in kaikkikortit:

            tunnistetutkadet.append(tunnista_texu(kortit + vaihtuvapoyta))

        max_value = max(tunnistetutkadet, key = lambda x : x[1][0])


        jakajat = 0

        for kasi in tunnistetutkadet:
            if kasi[1][0] == max_value[1][0]:
                jakajat += 1


        if jakajat == 1:
            index = tunnistetutkadet.index(max_value)
            pisteet[index][0] += 1

        elif jakajat > 1:
            for i in range(len(tunnistetutkadet)):
                if tunnistetutkadet[i][1][0] == max_value[1][0]:
                    pisteet[i][1] += 1/jakajat

        else:
            print("virhe620")
        
        testi += 1

    print("")

    return kaikkikortit, pisteet, poyta, tarkkuus

def peli(): 
    """
    Kaikki laskimelle annettavat inputit kysyvä pääfunktio.
    """
    pakka = luo_pakka()

    sekoitettupakka = sekoita_pakka(pakka)

    hero_kortit, sekoitettupakka = hero_kysely(sekoitettupakka)

    vihukorttilista = []

    i = 0

    while i < 9:
        
        try:
            villainkortit, sekoitettupakka = villain_kysely(sekoitettupakka, i)
        except:
            pelaajia = len(vihukorttilista)
            if pelaajia == 0:
                print(f"Tarvitaan vähintään yksi vastapelaaja.")
                continue
            break

        vihukorttilista.append(villainkortit)

        i += 1

    poytakortit = poyta(sekoitettupakka)
    pelaajia = len(vihukorttilista)

    return hero_kortit, vihukorttilista, sekoitettupakka, poytakortit, pelaajia

def testimaara():
    """
    Ohjelman tarkkuuden (0 -3) kysyva funktio. Tarkkuudella 3, tulos tallennetaan myös myöhemmin käytettäväksi.
    """
    try:
        print(f"\nValitse tarkkuus, jolla haluat käden todennäköisyydet laskea. (0 - 3)")
        tarkkuus = int(input(f"0 = Arvotaan kerran, 1 = Nopea, 2 = Normaali, 3 = Tarkka* (*Tulos tallennetaan)\n"))
    except:
        print(f"\nVastauksen tulee olla numero väliltä 1 - 3. Yritä uudestaan!\n")
        return testimaara()
    if tarkkuus == 0:
        return 1
    elif tarkkuus == 1:
        return 3000
    elif tarkkuus == 2:
        return 10000
    elif tarkkuus == 3:
        return 25000
    else:
        print(f"Kelvoton vastaus. Yritä uudestaan!")
        return testimaara()

def pelaajamaara(): 
    """
    Pelaajamäärän kysyvä funktio. Nykyversiossa ei käytössä mutta säilytän myöhemmän varalle.
    """
    try:
        pelaajia = int(input(f"\nMontako pelaajaa kädessä on mukana? (2 - 9)\n"))
    except:
        print(f"\nVastauksen tulee olla numero väliltä 2 - 9. Yritä uudestaan!\n")
        return pelaajamaara()

    if pelaajia >= 2 and pelaajia <= 9:
        return pelaajia
    else:
        print(f"\nKelvoton vastaus. Pelaajia tulee olla 2 - 9. Yritä uudestaan!\n")
        return pelaajamaara()

def maa_muunnokset(tallennusrivi: str, kuvakkeiksi: bool): 
    """
    Tallennusta varten ascii kuvakkeiden muuntaminen tekstiksi ja takaisin (true/false)
    """
    x = tallennusrivi

    if kuvakkeiksi == True:
        x = x.replace("♥","hertta")
        x = x.replace("♠","pata")
        x = x.replace("♦","ruutu")
        x = x.replace("♣","risti")
    
    if kuvakkeiksi == False:
        x = x.replace("hertta","♥")
        x = x.replace("pata","♠")
        x = x.replace("ruutu","♦")
        x = x.replace("risti","♣")

    return x
    
def tallennus(tallennusavain, tallennustulos, tarkkuus):
    """
    Jos laskimen tarkkuudeksi valittu 3, tallentaa tuloksen.
    """
    tallennusrivi = str(tallennusavain)+"*****"+str(tallennustulos)

    if tarkkuus >= 15000:

        with open("tallennus.txt","a") as historia:
            x = maa_muunnokset(tallennusrivi, True)
            historia.write(str(x)+"\n")
    
    else:
        pass

def haku(tallennusavain):
    """
    Kun laskettavan käden tiedot on syötetty, ennen kuin laskua aletaan tekemään, tämä tarkistaa onko samasta kädestä aiemmin tallennettua tulosta olemassa.
    """
    x = maa_muunnokset(tallennusavain, True)
    try:
        with open("tallennus.txt") as historia:
            tallennus = historia.readlines()
            for rivi in tallennus:
                avain, tulos = rivi.split("*****")
                if avain == x:
                    return tulos
    except:                                             #varmaankin kamala tapa toteuttaa, mutta tällä jos ei tallennustiedostoa löydy valmiiksi, luo sen.
        with open("tallennus.txt","a") as historia:
            with open("tallennus.txt") as historia:
                tallennus = historia.readlines()
                for rivi in tallennus:
                    avain, tulos = rivi.split("*****")
                    if avain == x:
                        return tulos
                               
def tuloksen_purku(tulos_tallennetuista):
    """
    Jos tallennettu tulos löytyy, tämä purkaa kyseisen rivin tallennustiedostosta ohjelman luettavaan muotoon.
    """
    maat_palautettu = maa_muunnokset(tulos_tallennetuista, False)

    x = maat_palautettu.split(",,,")
    kaikkikortit = x[0]
    pisteet = x[1]
    poyta = x[2]
    tarkkuus = x[3]

    return kaikkikortit, pisteet, poyta, int(tarkkuus)

def pisteiden_kasittely(pisteetkasittelematta):
    """
    Lisäfunktio tuloksen purkuun, muuttaa tallennustiedostosta saadun stringin jossa tulokset takaisin listaksi jossa 2 listaa, eli muotoon josta ohjelma tulostaa tulokset näkyville
    """
    kasitellytpisteet = ast.literal_eval(pisteetkasittelematta)

    return kasitellytpisteet

def korttientulostus(x):
    """
    Muuttaa kortit tulostaessa tupleista värillisiksi ja poistaa sulkeet sekä heittomerkit 
    """
    pakka = [(2, '♥'), (3, '♥'), (4, '♥'), (5, '♥'), (6, '♥'), (7, '♥'), (8, '♥'), (9, '♥'), (10, '♥'),
             (11, '♥'), (12, '♥'), (13, '♥'), (14, '♥'), (2, '♠'), (3, '♠'), (4, '♠'), (5, '♠'), (6, '♠'),
             (7, '♠'), (8, '♠'), (9, '♠'), (10, '♠'), (11, '♠'), (12, '♠'), (13, '♠'), (14, '♠'), (2, '♦'),
             (3, '♦'), (4, '♦'), (5, '♦'), (6, '♦'), (7, '♦'), (8, '♦'), (9, '♦'), (10, '♦'), (11, '♦'),
             (12, '♦'), (13, '♦'), (14, '♦'), (2, '♣'), (3, '♣'), (4, '♣'), (5, '♣'), (6, '♣'), (7, '♣'),
             (8, '♣'), (9, '♣'), (10, '♣'), (11, '♣'), (12, '♣'), (13, '♣'), (14, '♣')]
    
    #värilliset kuvakkeet, toimii vain vscodessa
    tulostuspakka = ["2 \033[1;31;38m♥\033[0m", "3 \033[1;31;38m♥\033[0m", "4 \033[1;31;38m♥\033[0m", "5 \033[1;31;38m♥\033[0m",
                     "6 \033[1;31;38m♥\033[0m", "7 \033[1;31;38m♥\033[0m", "8 \033[1;31;38m♥\033[0m", "9 \033[1;31;38m♥\033[0m",
                     "T \033[1;31;38m♥\033[0m", "J \033[1;31;38m♥\033[0m", "Q \033[1;31;38m♥\033[0m", "K \033[1;31;38m♥\033[0m",
                     "A \033[1;31;38m♥\033[0m", "2 \033[1;30;38m♠\033[0m", "3 \033[1;30;38m♠\033[0m", "4 \033[1;30;38m♠\033[0m",
                     "5 \033[1;30;38m♠\033[0m", "6 \033[1;30;38m♠\033[0m", "7 \033[1;30;38m♠\033[0m", "8 \033[1;30;38m♠\033[0m",
                     "9 \033[1;30;38m♠\033[0m", "T \033[1;30;38m♠\033[0m", "J \033[1;30;38m♠\033[0m", "Q \033[1;30;38m♠\033[0m",
                     "K \033[1;30;38m♠\033[0m", "A \033[1;30;38m♠\033[0m", "2 \033[1;34;38m♦\033[0m", "3 \033[1;34;38m♦\033[0m",
                     "4 \033[1;34;38m♦\033[0m", "5 \033[1;34;38m♦\033[0m", "6 \033[1;34;38m♦\033[0m", "7 \033[1;34;38m♦\033[0m",
                     "8 \033[1;34;38m♦\033[0m", "9 \033[1;34;38m♦\033[0m", "T \033[1;34;38m♦\033[0m", "J \033[1;34;38m♦\033[0m",
                     "Q \033[1;34;38m♦\033[0m", "K \033[1;34;38m♦\033[0m", "A \033[1;34;38m♦\033[0m", "2 \033[1;32;38m♣\033[0m",
                     "3 \033[1;32;38m♣\033[0m", "4 \033[1;32;38m♣\033[0m", "5 \033[1;32;38m♣\033[0m", "6 \033[1;32;38m♣\033[0m",
                     "7 \033[1;32;38m♣\033[0m", "8 \033[1;32;38m♣\033[0m", "9 \033[1;32;38m♣\033[0m", "T \033[1;32;38m♣\033[0m",
                     "J \033[1;32;38m♣\033[0m", "Q \033[1;32;38m♣\033[0m", "K \033[1;32;38m♣\033[0m", "A \033[1;32;38m♣\033[0m"]

    tulostuspakka_ei_vareja = 	["2 ♥", "3 ♥", "4 ♥", "5 ♥",
                                 "6 ♥", "7 ♥", "8 ♥", "9 ♥",
                                 "T ♥", "J ♥", "Q ♥", "K ♥",
                                 "A ♥", "2 ♠", "3 ♠", "4 ♠",
                                 "5 ♠", "6 ♠", "7 ♠", "8 ♠",
                                 "9 ♠", "T ♠", "J ♠", "Q ♠",
                                 "K ♠", "A ♠", "2 ♦", "3 ♦",
                                 "4 ♦", "5 ♦", "6 ♦", "7 ♦",
                                 "8 ♦", "9 ♦", "T ♦", "J ♦",
                                 "Q ♦", "K ♦", "A ♦", "2 ♣",
                                 "3 ♣", "4 ♣", "5 ♣", "6 ♣",
                                 "7 ♣", "8 ♣", "9 ♣", "T ♣",
                                 "J ♣", "Q ♣", "K ♣", "A ♣"]

    paluu = ""

    for i in x:
        index = pakka.index(i)
        paluu += str(tulostuspakka_ei_vareja[index])
        paluu += " "

    return paluu

def main():
    """
    Kaiken pääfunktio & tallennus
    """
    hero_kortit, villainkortit, sekoitettupakka, poytakortit, pelaajia = peli()         #Kyselyt

    tarkkuus = testimaara()                                                             #Asetukset

    tallennusavain = str(hero_kortit)+",,,"+str(villainkortit)+",,,"+str(poytakortit)   #Tallennusavaimen muodostus

    tulos_tallennetuista = haku(tallennusavain)                                         #Katsoo onko saman käden tulosta jo tallennettuna


    if (tulos_tallennetuista == None) or (tarkkuus == 1):                               #Jos kättä ei ole tallennettuna ennestään tai halutaan vain arpoa kerran
        
        if len(poytakortit) == 5:                                                       #jos pöytäkortteja 5, ei tarvetta laskea enempää kuin kerran, eikä tallentaa kun niin nopeaa               
            tarkkuus = 1

        kaikkikortit, pisteet, poyta, tarkkuus = testi(hero_kortit, villainkortit, sekoitettupakka, poytakortit,tarkkuus) # TESTI

        tallennustulos = str(kaikkikortit)+",,,"+str(pisteet)+",,,"+str(poyta)+",,,"+str(tarkkuus)  # Tallennustuloksen tallennus 

        tallennus(tallennusavain, tallennustulos, tarkkuus)                                         #tallennus jos tarkkuus on riittävä


    else:                                                                               #jos käsi on tallennettuna ennestään

        kaikkikortit, pisteetkasittelematta, poytakasittelematta, tarkkuus = tuloksen_purku(tulos_tallennetuista)

        kaikkikortit = [hero_kortit] + villainkortit                                    

        pisteet = pisteiden_kasittely(pisteetkasittelematta)

        poyta = poytakortit

    tulos(kaikkikortit, pisteet, poyta, tarkkuus)                                       #Tulostaa tuloksen käyttäjän nähtäväksi

    uudestaan()                                                                         #Uusi käsi / lopetus

if __name__ == "__main__":
    main()
