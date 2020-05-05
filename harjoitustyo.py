import numpy, os, re, ikkunasto
from matplotlib import pyplot as plt

TIEDOSTONIMEN_ALKUOSA = "measurement_"
TIEDOSTOPAATE = ".txt"
elementit = {"tekstilaatikko": None, "piirretty": 0, "alkupiste": [], "loppupiste": [], "ali_ikkuna": None}
energiat = []
intensiteettispektrien_summat = []


def atoi(alkio):
    return int(alkio) if alkio.isdigit() else alkio
    
    
def avaimet(tiedostolista):
    return [ atoi(alkio) for alkio in re.split("(\d+)",tiedostolista) ]
    
    
    
def lue_data(polku):
    """
    Lukee kaikki tekstitiedostot annetusta kansiosta, jotka ovat muotoa measure_nro.txt. Ohittaa tiedostot, jotka eivät
    ole kuvattua muotoa sekä tiedostot, joiden sisältämässä datassa on
    virheitä. Rikkinäisten tiedostojen nimet ilmoitetaan käyttäjälle.
    """

    try:
        tiedostot = os.listdir(polku)
        tiedostot.sort(key=avaimet)
    except FileNotFoundError:
        ikkunasto.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Datan luku epäonnistui. Yritä uudelleen.")
    
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
        
            tiedostopolku = os.path.join(polku, tiedosto)
            if tiedosto == tiedostonimi and len(intensiteettispektrien_summat) >= 1:
                with open(tiedostopolku, "r") as t:
                    rivit = t.readlines()
                    for j, rivi in enumerate(rivit):
                        aputaulukko = rivi.strip("\n").split(" ")
                        if len(aputaulukko) != 2:
                            virheelliset_tiedostot.append(tiedosto)
                            break
                        if float(aputaulukko[0]) not in energiat:
                            energiat.append(float(aputaulukko[0]))
                        intensiteettispektrien_summat[j] = intensiteettispektrien_summat[j] + float(aputaulukko[1])
                    if tiedosto not in virheelliset_tiedostot:
                        tiedostojen_lkm += 1
                    
                    
            elif tiedosto == tiedostonimi and len(intensiteettispektrien_summat) < 1:
                with open(tiedostopolku, "r") as t:
                    rivit = t.readlines()
                    for j, rivi in enumerate(rivit):
                        aputaulukko = rivi.strip("\n").split(" ")
                        if len(aputaulukko) != 2:
                            virheelliset_tiedostot.append(tiedosto)
                            break
                        if float(aputaulukko[0]) not in energiat:
                            energiat.append(float(aputaulukko[0]))
                        intensiteettispektrien_summat.append(float(aputaulukko[1]))

                    if tiedosto not in virheelliset_tiedostot:
                        tiedostojen_lkm += 1
            

        ikkunasto.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Luettiin " + str(tiedostojen_lkm) + " tiedostoa")


def avaa_kansio():
    """
    Napinkäsittelijä, joka pyytää käyttäjää valitsemaan kansion avaamalla
    kansioselaimen. Lataa datan valitusta kansiosta ja ilmoittaa käyttöliittymän
    tekstilaatikkoon montako riviä luettiin sekä virheellisten tiedostojen nimet.
    """ 
    lue_data(ikkunasto.avaa_hakemistoikkuna("Tiedostoselain"))


def piirra_kuvaaja():

    if len(energiat) < 1 and len(intensiteettispektrien_summat) < 1:
        ikkunasto.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Lataa ensin data.")
    elif elementit["piirretty"] > 0:
        ikkunasto.nayta_ali_ikkuna(elementit["ali_ikkuna"], "Kuvaaja")
        #ikkunasto.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Kuva on jo piirretty.")
    else:
        elementit["ali_ikkuna"] = ikkunasto.luo_ali_ikkuna("Kuvaaja")
        elementit["piirtoalue"], elementit["kuvaaja"] = ikkunasto.luo_kuvaaja(elementit["ali_ikkuna"], valitse_datapisteet, 640, 400)
        ax = elementit["kuvaaja"].add_subplot()
        ax.plot(energiat, intensiteettispektrien_summat)
        ax.set(xlabel="Sidosenergia (eV)", ylabel="Intensiteetti (mielivaltainen yksikkö)", title="Argonin spektri")
        elementit["piirretty"] = 1


def poista_lineaarinen_tausta():
    if len(energiat) < 1 and len(intensiteettispektrien_summat) < 1:
        ikkunasto.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Lataa ensin data.")
    #todo
    


def laske_piikkien_intensiteetit():
    if len(energiat) < 1 and len(intensiteettispektrien_summat) < 1:
        ikkunasto.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Lataa ensin data.")
    #todo


def tallenna_kuvaaja():
    if len(energiat) < 1 and len(intensiteettispektrien_summat) < 1:
        ikkunasto.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Lataa data ennen tallennusta.")
    else:
        try:
            tallennus_nimella = ikkunasto.avaa_tallennusikkuna("Tallenna nimellä")
            elementit["kuvaaja"].savefig(tallennus_nimella)
            if len(tallennus_nimella) > tallennus_nimella.rfind(".") and tallennus_nimella.rfind(".") > -1:
                ikkunasto.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Tiedosto tallennettiin nimellä: " + tallennus_nimella)
            else:
                ikkunasto.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "Tiedosto tallennettiin nimellä: " + tallennus_nimella + ".png")
        except ValueError:
            ikkunasto.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], "\nTallennus epäonnistui. Tallenna nimellä, esim. 'Kuvaaja', tai tiedostopääteen kera. Sallitut tiedostopäätteet ovat: .eps, .pdf, .pgf, .png, .ps, .raw, .rgba, .svg ja .svgz.")


def valitse_datapisteet(hiiritapahtuma):
    #nyt tallentuu sama piste molempiin
    elementit["alkupiste"].append((hiiritapahtuma.xdata, hiiritapahtuma.ydata))
    elementit["loppupiste"].append((hiiritapahtuma.xdata, hiiritapahtuma.ydata))
    #viesti = "Käyrän arvo pisteessä x={:.2f} on {:.2f}".format(tila["pisteet"][-1][0], tila["pisteet"][-1][1]) 
    #ikkunasto.kirjoita_tekstilaatikkoon(tila["tekstilaatikko"], viesti)
    ikkunasto.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"], str(elementit["alkupiste"]) +", " + str(elementit["loppupiste"]))
    


if __name__ == "__main__":
    ikkuna = ikkunasto.luo_ikkuna("File Browser by Jani Mynttinen")
    vasenkehys = ikkunasto.luo_kehys(ikkuna, ikkunasto.VASEN)
    oikea_ylakehys = ikkunasto.luo_kehys(ikkuna, ikkunasto.YLA)
    oikea_alakehys = ikkunasto.luo_kehys(ikkuna, ikkunasto.YLA)
    nappikehys = ikkunasto.luo_kehys(vasenkehys, ikkunasto.VASEN)
    lataanappi = ikkunasto.luo_nappi(nappikehys, "Lataa data", avaa_kansio)
    piirranappi = ikkunasto.luo_nappi(nappikehys, "Piirrä kuvaaja", piirra_kuvaaja)
    poista_lineaarinen_tausta_nappi = ikkunasto.luo_nappi(nappikehys, "Poista lineaarinen tausta", poista_lineaarinen_tausta)
    piikkien_intensiteetit_nappi = ikkunasto.luo_nappi(nappikehys, "Laske piikkien intensiteetit", laske_piikkien_intensiteetit)
    tallenna_kuvaaja_nappi = ikkunasto.luo_nappi(nappikehys, "Tallenna kuvaaja", tallenna_kuvaaja)
    lopetanappi = ikkunasto.luo_nappi(nappikehys, "Lopeta", ikkunasto.lopeta)
    elementit["tekstilaatikko"] = ikkunasto.luo_tekstilaatikko(oikea_ylakehys)
    
    
    
    ikkunasto.kaynnista()
