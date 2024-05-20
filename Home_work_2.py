# Část 1 - vyhledavani informace o konkrétním subjektu na základě jeho identifikačního čísla (IČO)
import requests

ICO = input('Dobry den, prosim zadejte ICO subjektu o kterém chce získat informace: ')
url= 'https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/ICO'
urlwithinputico=url.replace('ICO',(ICO))
response = requests.get(urlwithinputico)
data_1 = response.json()
print(data_1['obchodniJmeno'])
print(data_1['sidlo']['textovaAdresa'])

# Část 2 - program, který se zeptá uživatele(ky) na název subjektu, který chce vyhledat

headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
}
company_from_user=input('Dobry den, prosim napiste název subjektu, který chce vyhledat: ')
data_2 = {"obchodniJmeno": company_from_user}
res = requests.post("https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat", headers=headers, json=data_2)
data_3=res.json()

if 'pocetCelkem'in data_3:
    print(f"Nalezeno subjektů: {data_3['pocetCelkem']}")
else:
    print("Nazev subjektu nebyl nalezen.")

# Část 3 - právní forma

data_4= '{"kodCiselniku": "PravniForma", "zdrojCiselniku": "res"}'
res = requests.post("https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ciselniky-nazevniky/vyhledat", headers=headers, data=data_4)
data_5=res.json()
ciselniky = data_5['ciselniky']
ciselnik = ciselniky[0]
polozky_ciselniku = ciselnik['polozkyCiselniku']

def find_legal_form(kod,polozky_ciselniku):
    for polozka in polozky_ciselniku:
        if polozka['kod'] == kod:
            return polozka['nazev'][0]['nazev']
    return "Nenalezeno"

if 'ekonomickeSubjekty' in data_3:
    for subject in data_3['ekonomickeSubjekty']:
        company_name = subject.get('obchodniJmeno')
        ico = subject.get('ico')
        pravni_forma=subject.get('pravniForma')
        pravni_forma_text = find_legal_form(pravni_forma, polozky_ciselniku)
        print(f"{company_name}, {ico}, {pravni_forma_text}")
else:
    print("Nazev subjektu nebyl nalezen.")
