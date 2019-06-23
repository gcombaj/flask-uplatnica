# -*- coding: utf-8 -*
import sys
sys.path.append('..')

from uplatnica import *

####################### TEST ##############################

testni_podaci = """
                {
                "poziv_na_broj_platitelja": "",
                "poziv_na_broj_primatelja": "12345-212-2",
                "iznos": "12345",
                "iban_primatelja": "HR9223600001501426697",
                "iban_platitelja": "",
                "model_primatelja": "HR01",
                "model_platitelja": "",
                "sifra_namjene": "",
                "datum_izvrsenja": "10022016",
                "valuta_placanja": "HRK",
                "hitno": "",
                "ime_i_prezime_platitelja": "Pero Perić",
                "ulica_i_broj_platitelja": "Ilica 1",
                "postanski_i_grad_platitelja": "10000 Zagreb",
                "naziv_primatelja": "Sklonište za nezbrinute životinje",
                "ulica_i_broj_primatelja": "Franjčevićeva 43",
                "postanski_i_grad_primatelja": "10361 Dumovec",
                "opis_placanja": "Novčani prilog za pomoć nezbrinutim životinjama."}
                """

uplatnica = kreiraj_uplatnicu(testni_podaci)

open('demo_uplatnica.pdf', 'wb').write(uplatnica)
