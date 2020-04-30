import matplotlib, numpy, os, re, ikkunasto

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
    tiedostot = os.listdir(polku)
    tiedostot.sort(key=avaimet)

    energiat = []
    intensiteettispektrien_summat = []
    tiedostonimen_alkuosa = "measurement_"
    tiedostopaate = ".txt"
    for i, tiedosto in enumerate(tiedostot):
        tiedostonimi = tiedostonimen_alkuosa + str(i), tiedostopaate # tätä täytyy vielä säätää: alkuosa, leikkaus tiedostopäätteeseen asti, onko leikkaus nro? tms...
        summa = 0
        
        if tiedosto == tiedostonimi and intensiteettispektrien_summat != "":
            with open(tiedosto, "r") as t:
                rivit = t.readlines()
                for j, rivi in enumerate(rivit):
                    aputaulukko = rivi.strip("\n").split(" ")
                    
                    if aputaulukko[0] not in energiat:
                        energiat.append(aputaulukko[0])
                    else:
                        continue
                    intensiteettispektrien_summat[j] = intensiteettispektrien_summat[j] + aputaulukko[1]
                    
                    
        elif tiedosto == tiedostonimi and intensiteettispektrien_summat == "":
            with open(tiedosto, "r") as t:
                rivit = t.readlines()
                for j, rivi in enumerate(rivit):
                    aputaulukko = rivi.strip("\n").split(" ")
                    if aputaulukko[0] not in energiat:
                        energiat.append(aputaulukko[0])
                    else:
                        continue
                    intensiteettispektrien_summat.append(aputaulukko[1])
            
    

    #return palautettava, vialliset

def avaa_kansio():
    """
    Napinkäsittelijä, joka pyytää käyttäjää valitsemaan kansion avaamalla
    kansioselaimen. Lataa datan valitusta kansiosta ja ilmoittaa käyttöliittymän
    tekstilaatikkoon montako riviä luettiin sekä virheellisten tiedostojen nimet.
    """
    sisalto, virheelliset = lue_data(ikkunasto.avaa_hakemistoikkuna("Tiedostoselain"))
    
    if len(virheelliset) > 0:
        for tiedosto in virheelliset:
            ikkunasto.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"],
            "Viallinen tiedosto: " + tiedosto)
    ikkunasto.kirjoita_tekstilaatikkoon(elementit["tekstilaatikko"],
    "Luettiin " + str(len(sisalto)) + " riviä dataa.")


def main():
        """
        Luo käyttöliittymäikkunan, jossa on vasemmalla kaksi nappia ja oikealla
        tekstilaatikko, johon nappia painamalla voidaan tulostaa tekstiä.
        """
        ikkuna = ikkunasto.luo_ikkuna("File Browser by Jani Mynttinen")
        vasenkehys = ikkunasto.luo_kehys(ikkuna, ikkunasto.VASEN)
        oikeakehys = ikkunasto.luo_kehys(ikkuna, ikkunasto.VASEN)
        nappikehys = ikkunasto.luo_kehys(vasenkehys, ikkunasto.VASEN)
        lataanappi = ikkunasto.luo_nappi(nappikehys, "Lataa data", avaa_kansio)
        lopetanappi = ikkunasto.luo_nappi(nappikehys, "Lopeta", ikkunasto.lopeta)
        elementit["tekstilaatikko"] = ikkunasto.luo_tekstilaatikko(oikeakehys, 80, 30)
        ikkunasto.kaynnista()
        
if __name__ == "__main__":
    main()
