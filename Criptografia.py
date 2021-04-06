# -*- coding: utf-8 -*-

import json
import string
import requests

from Crypto.Hash import SHA1  # pycryptodome


# Web Scraping
s_token = 'ea0722f5c070c43f04e8c5670e193c38933e605d'
contents = requests.get('https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=' + s_token)
arq_json = json.loads(contents.text, encoding='utf-8')
print(arq_json)
print(type(arq_json))

# Capturando texto cifrado
nro_casas = int(arq_json['numero_casas'])
cipher = arq_json['cifrado'].lower()
print(cipher)

# Decifrando o texto
letras = list(string.ascii_lowercase)
print(letras)

decipher = ''
for letra in cipher:
    if letra in letras:
        index = letras.index(letra) - nro_casas
        decipher += letras[index]
    else:
        decipher += letra

# Gravando texto decifrado
decipher = decipher.lower()
arq_json['decifrado'] = decipher
print(arq_json['decifrado'])

# Gravando hash SHA1
decipher = decipher.encode('utf-8')
hashSHA1 = SHA1.new(decipher).hexdigest()
arq_json['resumo_criptografico'] = hashSHA1
print(arq_json['resumo_criptografico'])
print(arq_json)

# Salvando arquivo resposta
with open('answer.json', 'w', encoding='utf-8') as f:
    json.dump(obj=arq_json, fp=f, indent=4, sort_keys=False)
    f.close()

# Submeter post do arquivo json resultante
urlpost = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token={0}'.format(s_token)
file = {"answer": open("answer.json", "rb")}
response = requests.post(urlpost, files=file)
print(response.status_code)
print(response.content)
print(response.text)
print(response.headers)
