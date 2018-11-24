# -*- coding: utf-8 -*
import jinja2
import json
import textwrap
import subprocess

from flask import Flask
from flask import request
from flask import send_file
from io import BytesIO




app = Flask(__name__)


@app.route("/",methods=[ 'POST'])
def hello():
    
    if request.is_json:
        uplatnica = kreiraj_uplatnicu(json.dumps(request.json))
        byte_io = BytesIO(uplatnica)
        return send_file(byte_io, mimetype='application/pdf')

    return 'error'


def kreiraj_uplatnicu(podaci):
    """
    Prima podatke u JSON formatu i vraća sadržaj PDF datoteke
    """
    podaci = json.loads(podaci)

    def sredi_znakove(value):
        rjecnik = {u'š': u'scaron', u'Š': u'Scaron',
                   u'ž': u'zcaron', u'Ž': u'Zcaron',
                   u'đ': u'dcroat', u'Đ': u'Dcroat',
                   u'ć': u'cacute', u'Ć': u'Cacute',
                   u'č': u'ccaron', u'Č': u'Ccaron'}

        for k, v in rjecnik.iteritems():
            value = value.replace(k, u') show /%s glyphshow (' % v)

        return value

    jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="./"))
    jinja.filters['sredi_znakove'] = sredi_znakove

    template = jinja.get_template("uplatnica.tpl")

    podaci['opis'] = map(sredi_znakove, textwrap.wrap(podaci['opis_placanja'], 28))
    podaci['textwrap'] = textwrap

    gs = subprocess.Popen(['gs', '-sOutputFile=-', '-sDEVICE=pdfwrite',
                           '-dPDFSETTINGS=/prepress', '-dHaveTrueTypes=true',
                           '-dEmbedAllFonts=true', '-dSubsetFonts=true', '-'],
                           stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    izlaz, greska = gs.communicate(template.render(podaci).encode('utf-8'))
    return izlaz

########################## TEST ##############################
#
# testni_podaci = """
#                  {
#                  "poziv_na_broj_platitelja": "",
#                  "poziv_na_broj_primatelja": "12345-212-2",
#                  "iznos": "12345",
#                  "iban_primatelja": "HR9223600001501426697",
#                  "iban_platitelja": "",
#                  "model_primatelja": "HR01",
#                  "model_platitelja": "",
#                  "sifra_namjene": "",
#                  "datum_izvrsenja": "10022016",
#                  "valuta_placanja": "HRK",
#                  "hitno": "",
#                  "ime_i_prezime_platitelja": "Pero Perić",
#                  "ulica_i_broj_platitelja": "Ilica 1",
#                  "postanski_i_grad_platitelja": "10000 Zagreb",
#                  "naziv_primatelja": "Sklonište za nezbrinute životinje",
#                  "ulica_i_broj_primatelja": "Franjčevićeva 43",
#                  "postanski_i_grad_primatelja": "10361 Dumovec",
#                  "opis_placanja": "Novčani prilog za pomoć nezbrinutim životinjama."}
#                 """

# uplatnica = kreiraj_uplatnicu(testni_podaci)

# open('demo_uplatnica.pdf', 'w').write(uplatnica)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)