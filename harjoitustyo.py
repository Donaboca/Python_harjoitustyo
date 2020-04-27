import matplotlib, numpy, ikkunasto




def main():
        """
        Luo käyttöliittymäikkunan, jossa on vasemmalla kaksi nappia ja oikealla
        tekstilaatikko, johon nappia painamalla voidaan tulostaa tekstiä.
        """
        ikkuna = ikkunasto.luo_ikkuna("File Browser by Jani")
        vasenkehys = ikkunasto.luo_kehys(ikkuna, ikkunasto.VASEN)
        oikeakehys = ikkunasto.luo_kehys(ikkuna, ikkunasto.VASEN)
        nappikehys = ikkunasto.luo_kehys(vasenkehys, ikkunasto.VASEN)
        lataanappi = ikkunasto.luo_nappi(nappikehys, "Lue data hakemistosta", avaa_kansio)
        lopetanappi = ikkunasto.luo_nappi(nappikehys, "Lopeta", ikkunasto.lopeta)
        elementit["tekstilaatikko"] = ikkunasto.luo_tekstilaatikko(oikeakehys, 80, 30)
        ikkunasto.kaynnista()
        
if __name__ == "__main__":
    main()
