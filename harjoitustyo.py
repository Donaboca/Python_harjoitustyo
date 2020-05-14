import os
import re
import numpy as np
import ikkunasto as ik


#Olen käyttänyt Anaconda-jakelun iPythonia.
#Matplotlib versio 3.2.1
#Numpy versio 1.18.3


TIEDOSTONIMEN_ALKUOSA = "measurement_"
TIEDOSTOPAATE = ".txt"
elementit = {"tekstilaatikko": None, "piirretty": 0, "alkupiste": [], "loppupiste": [],
             "ali_ikkuna": None, "kuvaaja": ik.Figure(figsize=(6.4, 4), dpi=100),
             "viesti": 0, "lineaarinen_tausta_tila": 0}
energiat = []
intensiteettispektrien_summat = []

# atoi ja avaimet -funktioista otettu mallia:
# https://www.tutorialspoint.com/How-to-correctly-sort-a-string-with-a-number-inside-in-Python

def atoi(alkio):
    """ascii to integer, palauttaa merkit integer-muodossa"""
    return int(alkio) if alkio.isdigit() else alkio

def avaimet(tiedostolista):
    """Järjestää parametrina saatavan tiedostolistan aakkosjärjestykseen siten,
    että numerot ovat numerojärjestyksessä"""
    return [atoi(alkio) for alkio in re.split("(\\d+)", tiedostolista)]

def lue_data(polku):
    """
    Lukee kaikki tekstitiedostot annetusta kansiosta, jotka ovat muotoa measure_nro.txt. Ohittaa
    tiedostot, jotka eivät ole kuvattua muotoa sekä tiedostot, joiden sisältämässä datassa on
    virheitä. Rikkinäisten tiedostojen nimet ilmoitetaan käyttäjälle.
    """
    tyhjenna_datapisteet("funktio")
    oikeat_energiat = []
    oikeat_intensiteetit = []
    elementit["piirretty"] = 0
    elementit["viesti"] = 0
    elementit["lineaarinen_tausta_tila"] = 0

    if len(energiat) > 0 or len(intensiteettispektrien_summat) > 0:
        energiat.clear()
        intensiteettispektrien_summat.clear()

    try:
        tiedostot = os.listdir(polku)
        tiedostot.sort(key=avaimet)
    except FileNotFoundError:
        ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Datan luku epäonnistui. Yritä uudelleen.")
        return oikeat_energiat, oikeat_intensiteetit

    else:
        virheelliset_tiedostot = []

        tiedostojen_lkm = 0

        for tiedosto in tiedostot:
            try:
                tiedostonimen_numero = tiedosto.split("_")[1].split(".")[0]
                if not tiedostonimen_numero.isdigit():
                    continue
                tiedostonimi = TIEDOSTONIMEN_ALKUOSA + str(tiedostonimen_numero) + TIEDOSTOPAATE
            except IndexError:
                continue
            energiat_apu = []
            intensiteetit_apu = []
            tiedostopolku = os.path.join(polku, tiedosto)
            if tiedosto == tiedostonimi and len(intensiteettispektrien_summat) >= 1:
                with open(tiedostopolku, "r") as tied:
                    rivit = tied.readlines()
                    for j, rivi in enumerate(rivit):
                        aputaulukko = rivi.strip("\n").split(" ")
                        if len(aputaulukko) != 2:
                            virheelliset_tiedostot.append(tiedosto)
                            energiat_apu.clear()
                            intensiteetit_apu.clear()
                            break
                        try:
                            energia_arvo = float(aputaulukko[0])
                            intensiteetti_arvo = float(aputaulukko[1])
                        except ValueError:
                            virheelliset_tiedostot.append(tiedosto)
                            energiat_apu.clear()
                            intensiteetit_apu.clear()
                            break
                        else:
                            #if energia_arvo not in energiat_apu:
                            energiat_apu.append(energia_arvo)
                            intensiteetit_apu[j] = intensiteetit_apu[j] + intensiteetti_arvo
                    if tiedosto not in virheelliset_tiedostot:
                        tiedostojen_lkm += 1
                    else:
                        ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Virheelinen tiedosto: " + virheelliset_tiedostot[-1])
                    if len(energiat_apu) > 0:
                        oikeat_energiat.append(energiat_apu)
                    if len(intensiteetit_apu) > 0:
                        oikeat_intensiteetit.append(intensiteetit_apu)

            elif tiedosto == tiedostonimi and len(intensiteettispektrien_summat) < 1:
                with open(tiedostopolku, "r") as tied:
                    rivit = tied.readlines()
                    for rivi in rivit:
                        aputaulukko = rivi.strip("\n").split(" ")
                        if len(aputaulukko) != 2:
                            virheelliset_tiedostot.append(tiedosto)
                            energiat_apu.clear()
                            intensiteetit_apu.clear()
                            break
                        try:
                            energia_arvo = float(aputaulukko[0])
                            intensiteetti_arvo = float(aputaulukko[1])
                        except ValueError:
                            virheelliset_tiedostot.append(tiedosto)
                            energiat_apu.clear()
                            intensiteetit_apu.clear()
                            break
                        else:
                            #if energia_arvo not in energiat_apu:
                            energiat_apu.append(energia_arvo)
                            intensiteetit_apu.append(intensiteetti_arvo)
                    if tiedosto not in virheelliset_tiedostot:
                        tiedostojen_lkm += 1
                    else:
                        ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Virheelinen tiedosto: " + virheelliset_tiedostot[-1])
                    if len(energiat_apu) > 0:
                        oikeat_energiat.append(energiat_apu)
                    if len(intensiteetit_apu) > 0:
                        oikeat_intensiteetit.append(intensiteetit_apu)

        ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Luettiin " + str(tiedostojen_lkm) + " tiedostoa")

        return oikeat_energiat, oikeat_intensiteetit

def avaa_kansio():
    """
    Napinkäsittelijä, joka pyytää käyttäjää valitsemaan kansion avaamalla
    kansioselaimen. Lataa datan valitusta kansiosta ja ilmoittaa käyttöliittymän
    tekstilaatikkoon montako riviä luettiin sekä virheellisten tiedostojen nimet.
    """
    energia_taulukko, intensiteetti_taulukko = lue_data(ik.avaa_hakemistoikkuna("Tiedostoselain"))
    for i in range(len(energia_taulukko)):
        for j in range(len(energia_taulukko[0])):
            if energia_taulukko[i][j] not in energiat:
                energiat.append(energia_taulukko[i][j])
            if i == 0:
                intensiteettispektrien_summat.append(intensiteetti_taulukko[i][j])
            else:
                intensiteettispektrien_summat[j] = intensiteettispektrien_summat[j] + intensiteetti_taulukko[i][j]

def piirra_kuvaaja():
    """
    Napinkäsittelijä piirtää kuvaajan luetun datan perusteella.
    Jos kuvaaja on piirretty aikaisemmin, niin sitten näytetään aiemmin piirretty kuvaaja.
    Piirtämisen jälkeen tyhjennetään datapisteet, jotta ne on valittavissa lineaarisen taustan
    poistamista varten tai mittaustulosten piikkien intensiteettien laskemiseksi.
    """
    if len(energiat) < 1 and len(intensiteettispektrien_summat) < 1:
        ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Lataa ensin data.")
    elif elementit["piirretty"] > 0:
        ik.nayta_ali_ikkuna(elementit["ali_ikkuna"], "Kuvaaja")
    else:
        elementit["ali_ikkuna"] = ik.luo_ali_ikkuna("Kuvaaja")
        elementit["piirtoalue"], elementit["kuvaaja"] = ik.luo_kuvaaja(elementit["ali_ikkuna"], valitse_datapisteet, 640, 400)
        ax = elementit["kuvaaja"].add_subplot()
        ax.plot(energiat, intensiteettispektrien_summat)
        ax.set(xlabel="Sidosenergia (eV)", ylabel="Intensiteetti", title="Argonin spektri")
        elementit["piirretty"] = 1
        tyhjenna_datapisteet("funktio")
        if elementit["viesti"] == 0:
            ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Valitse datapisteet lineaarisen taustan poistoa varten.")

def poista_lineaarinen_tausta():
    """
    Napinkäsittelijä, joka laskee annetun suoran pisteiden perusteella suoran
    kulmakertoimen sekä vakiotermin. Niiden ja x-akselin pisteiden avulla saadaan
    x-akselin arvoja vastaavat y-akselin pisteet. Lopuksi funtio laskee
    intensiteettispektreille uudet arvot, jotta lineaarinen tausta saadaan kuvaajasta pois.
    """

    if elementit["lineaarinen_tausta_tila"] == 1:
        ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Tausta on jo poistettu.")
    elif len(energiat) < 1 and len(intensiteettispektrien_summat) < 1:
        ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Lataa ensin data.")
    elif len(elementit["alkupiste"]) < 1 or len(elementit["loppupiste"]) < 1:
        ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Valitse ensin datapisteet.")
    else:
        ik.piilota_ali_ikkuna(elementit["ali_ikkuna"])
        y_arvot_suoralla = []
        kulmakerroin = (elementit["loppupiste"][0][1] - elementit["alkupiste"][0][1]) / (elementit["loppupiste"][0][0] - elementit["alkupiste"][0][0])
        vakiotermi = (elementit["loppupiste"][0][0] * elementit["alkupiste"][0][1] - elementit["alkupiste"][0][0] * elementit["loppupiste"][0][1]) / (elementit["loppupiste"][0][0] - elementit["alkupiste"][0][0])
        for i in range(len(energiat)):
            y_arvot_suoralla.append(kulmakerroin * energiat[i] + vakiotermi)

        for i in range(len(intensiteettispektrien_summat)):
            intensiteettispektrien_summat[i] = intensiteettispektrien_summat[i] - y_arvot_suoralla[i]
        elementit["piirretty"] = 0
        elementit["viesti"] = 1
        elementit["lineaarinen_tausta_tila"] = 1
        piirra_kuvaaja()
        tyhjenna_datapisteet("funktio")
        ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Valitse datapisteet piikkien intensiteettien laskemista varten.")

def laske_piikkien_intensiteetit():
    """
    Napinkäsittelijä, joka etsii suoran x-akselin pisteiden väliin osuvat mitatut
    energiat (x-akselin arvot) ja energioita vastaavat y-akselin arvot. Niitä
    hyödyntäen lasketaan piikin pinta-ala puolisuunnikassäännön avulla käyttäen
    Numpyn Trapz -funktiota. Pinta-ala kirjoitetaan käyttöliittymän tekstilaatikkoon.
    """
    if len(energiat) < 1 and len(intensiteettispektrien_summat) < 1:
        ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Lataa ensin data.")
    elif len(elementit["alkupiste"]) < 1 or len(elementit["loppupiste"]) < 1:
        ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Valitse ensin datapisteet.")
    elif elementit["lineaarinen_tausta_tila"] == 0:
        ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Poista ensin lineaarinen tausta.")
    else:

        if elementit["alkupiste"][0][0] > elementit["loppupiste"][0][0]:
            x_alku = elementit["loppupiste"][0][0]
            x_loppu = elementit["alkupiste"][0][0]
        else:
            x_alku = elementit["alkupiste"][0][0]
            x_loppu = elementit["loppupiste"][0][0]

        y_arvot_piikissa = []
        x_arvot_piikissa = []
        for i in range(len(energiat)):
            if energiat[i] >= x_alku and energiat[i] <= x_loppu:
                y_arvot_piikissa.append(intensiteettispektrien_summat[i])
                x_arvot_piikissa.append(energiat[i])
            elif energiat[i] > x_loppu:
                break
        ala = np.trapz(y_arvot_piikissa, x_arvot_piikissa)
        ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Piikin ala on: " + str(ala))

def tallenna_kuvaaja():
    """
    Napinkäsittelijä. Piirretty ja tai muistissa oleva kuvaaja tallennetaan
    käyttäjän antamaan sijaintiin. Käyttäjä voi antaa tiedostotyypin tallennusvaiheessa.
    Jos hän jättää sen antamatta, tiedosto tallennetaan .png -muodossa.
    """
    if len(energiat) < 1 and len(intensiteettispektrien_summat) < 1:
        ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Lataa data ennen tallennusta.")
    else:
        try:
            tallennus_nimella = ik.avaa_tallennusikkuna("Tallenna nimellä")
            if not tallennus_nimella:
                ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Tiedoston tallennus keskeytyi.")
            else:
                elementit["kuvaaja"].savefig(tallennus_nimella)
                if len(tallennus_nimella) > tallennus_nimella.rfind(".") and tallennus_nimella.rfind(".") > -1:
                    ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Tiedosto tallennettiin nimellä: " + tallennus_nimella)
                else:
                    ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Tiedosto tallennettiin nimellä: " + tallennus_nimella + ".png")
        except ValueError:
            ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Tallennus epäonnistui. Tallenna nimellä, esim. 'Kuvaaja', tai tiedostopääteen kera. Sallitut tiedostopäätteet ovat: .eps, .pdf, .pgf, .png, .ps, .raw, .rgba, .svg ja .svgz.")

def valitse_datapisteet(hiiritapahtuma):
    """
    Käyttäjä voi valita kuvaajassa datapisteet. Niiden avulla poistetaan kuvaajassa ilmenevä
    lineaarinen tausta tai lasketaan kuvaajan piikkien pinta-ala. Valitut datapisteet ilmoitetaan
    ohjelman tekstilaatikossa.
    """
    if len(elementit["alkupiste"]) < 1:
        elementit["alkupiste"].append((hiiritapahtuma.xdata, hiiritapahtuma.ydata))
        if elementit["alkupiste"][0][0] is None and elementit["alkupiste"][0][1] is None:
            elementit["alkupiste"] = []
        else:
            ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Valitsemasi alkupiste: " + str(elementit["alkupiste"][0][0]) + ", " + str(elementit["alkupiste"][0][1]))
    elif len(elementit["loppupiste"]) < 1:
        elementit["loppupiste"].append((hiiritapahtuma.xdata, hiiritapahtuma.ydata))
        if elementit["loppupiste"][0][0] is None and elementit["loppupiste"][0][1] is None:
            elementit["loppupiste"] = []
        else:
            ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Valitsemasi loppupiste: " + str(elementit["loppupiste"][0][0]) + ", " + str(elementit["loppupiste"][0][1]))
    else:
        ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Olet jo valinnut suoran pisteet!")

def tyhjenna_datapisteet(kutsuja="painike"):
    """
    Tyhjentää kuvaajassa valitut suoran datapisteet.
    """
    if kutsuja == "funktio":
        elementit["alkupiste"] = []
        elementit["loppupiste"] = []
    elif len(elementit["alkupiste"]) > 0 or len(elementit["loppupiste"]) > 0:
        elementit["alkupiste"] = []
        elementit["loppupiste"] = []
        ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Datapisteet on tyhjennetty.")
    else:
        ik.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Ei löytynyt datapisteitä.")

def main():
    """
    Main-funktio toimii pääohjelmana.
    """
    ikkuna = ik.luo_ikkuna("File Browser by Jani Mynttinen")
    vasenkehys = ik.luo_kehys(ikkuna, ik.VASEN)
    oikea_ylakehys = ik.luo_kehys(ikkuna, ik.YLA)
    oikea_alakehys = ik.luo_kehys(ikkuna, ik.YLA)
    nappikehys = ik.luo_kehys(vasenkehys, ik.VASEN)
    ik.luo_nappi(nappikehys, "Lataa data", avaa_kansio)
    ik.luo_nappi(nappikehys, "Piirrä kuvaaja", piirra_kuvaaja)
    ik.luo_nappi(nappikehys, "Poista lineaarinen tausta", poista_lineaarinen_tausta)
    ik.luo_nappi(nappikehys, "Laske piikkien intensiteetit", laske_piikkien_intensiteetit)
    ik.luo_nappi(nappikehys, "Poista valitut datapisteet", tyhjenna_datapisteet)
    ik.luo_nappi(nappikehys, "Tallenna kuvaaja", tallenna_kuvaaja)
    ik.luo_nappi(nappikehys, "Lopeta", ik.lopeta)
    elementit["tekstilaatikko"] = ik.luo_tekstilaatikko(oikea_ylakehys)
    ik.kaynnista()

if __name__ == "__main__":
    main()
