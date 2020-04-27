# Python_harjoitustyo

Ohjelmassasi pitää olla seuraavat ominaisuudet:

Ohjelmassa on graafinen käyttöliittymä, josta käyttäjä voi valita ohjelman eri toiminnot.

Ensimmäinen toiminto lataa datan tiedostoista ohjelman muistiin. Aliohjelma etsii käyttäjän valitsemasta kansiosta tiedostoja, joiden nimi on ylläolevaa muotoa ja lukee niissä olevan datan. Aliohjelman tulee luoda ohjelmaan muistiin kaksi listaa, joista toisessa on mitatut kineettiset energiat ja toisessa summa jokaisesta mitatusta intensiteetispektristä. (Eli jokaista yksittäistä energiaa vastaavat intensiteetit eri mittauksista on laskettu yhteen.) Lopuksi aliohjelma ilmoittaa käyttäjälle montako tiedostoa ladattiin.

Toinen toiminto piirtää sen hetkisen ohjelman muistissa löytyvän datan näkyviin. Mikäli mitään dataa ei ole ladattu, tästä ilmoitetaan käyttäjälle jollain tavalla. Data piirretään näkyviin käyttämällä matplotlib-kirjastoa, ja käyttöliittymään upotettua kuvaajaa sekä piirtoaluetta - pyplotia ei siis vo käyttää. Kuvaajan pitäisi näyttää suurin piirtein alla olevan esimerkin mukaiselta.

Kolmas toiminto poistaa spektristä lineaarisen taustan. Mikäli mitään dataa ei ole ladattu ohjelman muistiin, ilmoitetaan tästä käyttäjälle. Käyttä valitsee kaksi pistettä klikkaamalla niitä kuvaajasta, ja ohjelma sovittaa näihin pisteisiin suoran sekä vähentää ohjelman muistissa olevasta spektristä taustan.

Neljäs toiminto laskee spektristä löytyvien piikkien intensiteetit. Mikäli mitään dataa ei ole ladattu ohjelman muistiin, ilmoitetaan tästä käyttäjälle. Integrointi tehdään käyttämällä puolisuunnikassääntöä, josta löytyy toteutus numpy-kirjastosta (numpy.trapz). Käyttäjä valitsee energiavälin klikkaamalla kuvaajasta. Tämän jälkeen ohjelma laskee piikin pinta-alan ja ilmoittaa sen käyttäjälle.

Viides toiminto antaa käyttäjän tallentaa kuvaajan ohjelman muistissa sillä hetkellä olevasta datasta. Mikäli mitään dataa ei ole ladattu ohjelman muistiin, ilmoitetaan tästä käyttäjälle. Aliohjelma kysyy käyttäjältä tiedostonnimen, jolla tämä haluaa kuvaajan tallentaa. Sen jälkeen aliohjelma tallentaa käyttäjän antamalla nimellä samanlaisen kuvaajan kuin mitä toisessa aliohjelmassa piirretään näkyviin. Kuvaajien tallentamiseen löytyy omat metodinsa matplotlib-kirjastosta. Kuvaajat voi tallentaa .png-muodossa.
