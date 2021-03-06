# -*- coding: utf-8 -*
import jinja2
import json
import textwrap
import subprocess

from flask import Flask
from flask import request
from flask import send_file
from io import BytesIO

import os


app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    demo_data = """
        Send this as POST in JSON format:
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
    return demo_data

@app.route("/",methods=['POST'])
def download_pdf():
    
    if request.is_json:
        paymentSlip = generate_payment_slip(json.dumps(request.json))
        byte_io = BytesIO(paymentSlip)
        return send_file(byte_io, mimetype='application/pdf')

    return 'error'


def generate_payment_slip(jsonInput):
    """
    Receives data in JSON and returns a PDF file
    """
    data = json.loads(jsonInput)

    def characterCleanup(value):
        characters = {u'š': u'scaron', u'Š': u'Scaron',
                   u'ž': u'zcaron', u'Ž': u'Zcaron',
                   u'đ': u'dcroat', u'Đ': u'Dcroat',
                   u'ć': u'cacute', u'Ć': u'Cacute',
                   u'č': u'ccaron', u'Č': u'Ccaron'}

        for k, v in characters.items():
            value = value.replace(k, u') show /%s glyphshow (' % v)

        return value
    
    currentDir = os.path.dirname(os.path.abspath(__file__))

    jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=currentDir + '/templates'))
    jinja.filters['characterCleanup'] = characterCleanup

    template = jinja.get_template("paymentSlip.tpl")

    data['opis'] = map(characterCleanup, textwrap.wrap(data['opis_placanja'], 28))
    data['textwrap'] = textwrap

    gs = subprocess.Popen(['gs', '-sOutputFile=-', '-sDEVICE=pdfwrite',
                           '-dPDFSETTINGS=/prepress', '-dHaveTrueTypes=true',
                           '-dEmbedAllFonts=true', '-dSubsetFonts=true', '-'],
                           stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    output, error = gs.communicate(template.render(data).encode('utf-8'))
    return output


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
    