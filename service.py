import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_text(city1, city2):
    input_text1 = city1
    if input_text1:
        #print(f"Textul introdus:{input_text}")
        id_value = make_api_requestname(input_text1)
        if id_value is not None:
            make_api_requestid(id_value,input_text1)
        else:
            print("Oras inexistent!")
    else:
        print("Textul introdus la orasul 1 este gol!")

    input_text2 = city2
    if input_text2:
        webscrape(input_text2)
    else:
        print("Textul introdus la orasul 2 este gol!")

    file1=fr"Path\To\Project\produse_combustibili_{input_text1}_API.csv"
    file2=fr"Path\To\Project\produse_combustibili_{input_text2}_webscraped.csv"
    city1=input_text1
    city2=input_text2
    compare_fuel_prices(file1, file2, city1, city2)
def save_to_csv(filename, data):
    """
    Creează un fișier CSV și salvează datele.
    :param filename: Numele fișierului CSV.
    :param data: Lista de date de salvat. Fiecare element este un tuple (produs, preț, benzinărie).
    """
    with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        # Scrie header-ul CSV
        writer.writerow(["Produs", "Preț", "Benzinărie"])
        # Scrie rândurile cu datele furnizate
        writer.writerows(data)
    print(f"Datele au fost salvate în fișierul {filename}")


def webscrape(cityname):
    # Configurare ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Rulează în fundal (opțional)
    chrome_options.add_argument("--disable-gpu")
    service = Service(r"Path\To\Project\chromedriver.exe")  # Actualizează calea către ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Accesează site-ul
        driver.get("https://www.peco-online.ro/index.php")

        # Găsește și apasă pe butonul de consimțământ (dacă există)
        try:
            consent_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "fc-button-label"))
            )
            consent_button.click()
            print("Consimțământul a fost acordat.")
        except Exception as e:
            print("Nu a fost găsit pop-up-ul de consimțământ, continuăm...")

        # Găsește textbox-ul după id și introduce numele orașului
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "nume_locatie"))
        )
        search_box.clear()
        search_box.send_keys(cityname)

        # Găsește și apasă butonul "Caută"
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Cauta')]"))
        )
        search_button.click()

        # Așteaptă încărcarea rezultatelor
        time.sleep(5)

        # Extrage datele din elementele <tr>
        rows = driver.find_elements(By.XPATH, "//tr")
        data = []
        for row in rows:
            try:
                # Extrage prețul
                price_element = row.find_element(By.XPATH, ".//span[contains(@class, 'pret')]")
                price = price_element.text

                # Extrage numele firmei
                firm_element = row.find_element(By.XPATH, ".//img[contains(@class, 'float-left')]")
                firm_name = firm_element.get_attribute("alt")

                # Adaugă datele în listă
                data.append({"price": price, "firm": firm_name})
            except Exception:
                # Ignoră rândurile care nu conțin informațiile dorite
                continue

        unique_data = []
        seen = set()

        for entry in data:
            key = (entry['price'],entry['firm'])
            if key not in seen:
                seen.add(key)
                unique_data.append(entry)

        # Afișează rezultatele
        for entry in unique_data:
            print(f"Preț: {entry['price']}, Firmă: {entry['firm']}")

        # Transformare în format tuple pentru funcția save_to_csv
        csv_data = [("Benzină standard", entry['price'], entry['firm']) for entry in unique_data]

        # Salvează datele în fișier CSV folosind funcția save_to_csv
        filename = f"produse_combustibili_{cityname}_webscraped.csv"
        save_to_csv(filename, csv_data)

    except Exception as e:
        print(f"A apărut o eroare: {e}")
    finally:
        driver.quit()



def make_api_requestname(uatname):
    url = f"https://monitorulpreturilor.info/pmonsvc/Gas/GetUATByName?uatname={uatname}"
    try:
        response = requests.get(url)
        #print(f"Status code: {response.status_code}")
        #print(f"Răspuns brut: {response.text}")

        if response.status_code == 200:
            # Verifică dacă răspunsul este XML
            if "application/xml" in response.headers["Content-Type"] or response.text.startswith('<?xml'):
                # Parsarea răspunsului XML
                try:
                    root = ET.fromstring(response.text)
                    #print("Răspuns API XML:", ET.tostring(root, encoding='unicode'))
                    ns = {'ns0': 'http://schemas.datacontract.org/2004/07/pmonsvc.Models.Protos'}  # Definirea namespace-ului
                    id_element = root.find('.//ns0:Id', ns)
                    if id_element is not None:
                        # Extragem valoarea din tag-ul <ns0:Id>
                        id_value = id_element.text
                        #print(f"ID extras:{id_value}")
                        # Poți folosi id_value pentru un alt request
                        return id_value
                    else:
                        print("Tag-ul <ns0:Id> nu a fost găsit.")
                except ET.ParseError as e:
                    print(f"Eroare la parsarea XML: {e}")
            else:
                print("Răspunsul nu este XML.")
        else:
            print(f"Eroare API: {response.status_code}")
    except Exception as e:
        print(f"Eroare la efectuarea requestului: {e}")


def make_api_requestid(id_value,uatname):
    url = f"https://monitorulpreturilor.info/pmonsvc/Gas/GetGasItemsByUat?UatId={id_value}&CSVGasCatalogProductIds=11&OrderBy=dist"
    try:
        response = requests.get(url)
        #print(f"Status code: {response.status_code}")
        #print(f"Răspuns brut:\n{response.text}")  # Afișează răspunsul brut pentru diagnosticare

        if response.status_code == 200:
            if "application/xml" in response.headers["Content-Type"] or response.text.startswith('<?xml'):
                try:
                    root = ET.fromstring(response.text)

                    # Definim namespace-ul
                    ns = {'ns': 'http://schemas.datacontract.org/2004/07/pmonsvc.Models.Protos'}

                    # Căutăm toate elementele <GasProduct> folosind namespace-ul
                    gas_products = root.findall('.//ns:GasProduct', ns)

                    if gas_products:
                        csv_data = []
                        #print("Produse găsite:")
                        for product in gas_products:
                            # Extragem datele din tag-urile relevante
                            name = product.find('.//ns:Name', ns).text if product.find('.//ns:Name', ns) is not None else "N/A"
                            price = product.find('.//ns:Price', ns).text if product.find('.//ns:Price', ns) is not None else "N/A"
                            #station_id = product.find('.//ns:Stationid', ns).text if product.find('.//ns:Stationid', ns) is not None else "N/A"
                            station_name = product.find('.//ns:Network/ns:Name', ns).text if product.find('.//ns:Network/ns:Name', ns) is not None else "N/A"
                            first_word = station_name.split()[0] if station_name else station_name

                            #print(f"Produs: {name}, Preț: {price}, Stație: {station_id}, Benzinărie: {station_name}")
                            csv_data.append((name, price, first_word))
                        csv_data = list(set(csv_data))
                        save_to_csv(f"produse_combustibili_{uatname}_API.csv", csv_data)
                    else:
                        print("Nu au fost găsite produse.")
                except ET.ParseError as e:
                    print(f"Eroare la parsarea XML: {e}")
            else:
                print("Răspunsul nu este XML.")
        else:
            print(f"Eroare API: {response.status_code}")
    except Exception as e:
        print(f"Eroare la efectuarea requestului: {e}")


def compare_fuel_prices(file1, file2, city1, city2):
    # Încărcăm fișierele CSV
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Normalizăm denumirile benzinăriilor (le facem toate litere mici)
    df1['Benzinărie_normalizată'] = df1['Benzinărie'].str.lower()
    df2['Benzinărie_normalizată'] = df2['Benzinărie'].str.lower()

    # Creăm o listă cu toate benzinăriile unice din ambele fișiere (fără a ține cont de litere mari/mici)
    all_stations = set(df1['Benzinărie_normalizată']).union(set(df2['Benzinărie_normalizată']))

    # Creăm un grafic cu bare
    bar_width = 0.35  # Lățimea barei
    index = np.arange(len(all_stations))  # Pozițiile pe axa X

    fig, ax = plt.subplots(figsize=(12, 6))

    # Pregătim datele pentru grafic
    for i, station in enumerate(all_stations):
        # Căutăm benzinăria în fiecare fișier, ținând cont doar de comparația între litere mici
        price_city1 = df1[df1['Benzinărie_normalizată'] == station]['Preț'].mean() if station in df1['Benzinărie_normalizată'].values else None
        price_city2 = df2[df2['Benzinărie_normalizată'] == station]['Preț'].mean() if station in df2['Benzinărie_normalizată'].values else None

        if price_city1 is not None:
            bar1 = ax.bar(index[i], price_city1, bar_width, color='red', alpha=0.7)
            ax.text(index[i], price_city1 + 0.1, f'{price_city1:.2f}', ha='center', va='bottom', color='black')

        if price_city2 is not None:
            bar2 = ax.bar(index[i] + bar_width, price_city2, bar_width, color='blue', alpha=0.7)
            ax.text(index[i] + bar_width, price_city2 + 0.1, f'{price_city2:.2f}', ha='center', va='bottom', color='black')

    ax.set_xlabel('Benzinărie')
    ax.set_ylabel('Preț (RON)')
    ax.set_title(f'Comparație prețuri benzină între {city1} și {city2}')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels([station.capitalize() for station in all_stations], rotation=45)

    # Legenda cu doar orașele
    ax.legend([bar1, bar2], [f'{city1}', f'{city2}'], loc='upper left')

    plt.tight_layout()
    plt.show()
