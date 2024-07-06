import requests
import time
from bs4 import BeautifulSoup
import json
import re
from threading import Thread
import os
from pathlib import Path

#file con i link su cui fare scraping
source_url="https://jp.pokellector.com/sets"

#percorso assuluto file corrente
file_path = os.path.dirname(Path(__file__).absolute())

#file json su cui scrivere i dati
dest_file = os.path.join(file_path, "./scraper_data/scraper.json")
dest_file = os.path.realpath(dest_file) #rimuove i ..

#calcolo path assoluto img
img_folder_path = os.path.join(file_path, "./scraper_data/img")
img_folder_path = os.path.realpath(img_folder_path) #rimuove i ..

#calcolo path assoluto img/cards
card_img_folder_path = os.path.join(file_path, "./scraper_data/img/cards")
card_img_folder_path = os.path.realpath(card_img_folder_path) #rimuove i ..

#calcolo path assoluto img/subsets_logo
logo_folder_path = os.path.join(file_path, "./scraper_data/img/sets_logo")
logo_folder_path = os.path.realpath(logo_folder_path) #rimuove i ..

#lista che contiene tutti i dati e che verrà stampata sul file json
sets_data=[]

#crea le cartelle richieste
def folder_setup():
    
    if not os.path.isdir(card_img_folder_path):
        os.mkdir(card_img_folder_path)
        print("Creata cartella per download immagini carte")
    else:
        print("Cartella per immagini carte esistente")

    if not os.path.isdir(logo_folder_path):
        os.mkdir(logo_folder_path)
        print("Creata cartella per download loghi espansioni")
    else:
        print("Cartella per loghi espansioni esistente")

#funzione dedicata al download delle immagini
def img_download(url, download_path, img_type = "card"):

    if url == "": #se l'url non e' stato definito per qualche motivo
        return url

    if "placeholder" in url: #se non esiste l'immagine di una carta
        return url

    #calcolo nome immagine a partire da url
    img_name = re.split("/|\.",url) #nome dell'immagine contenuto in posizione 6 e codice carta in posizione 8 (se si tratta di immagine carta)

    thumb_path = full_size_path = ""

    #percorso completo dell'immagine
    if(img_type == "card"):

        #sistema nome immagine per pokedrop-price-manager
        card_code = img_name[8]
        if len(card_code) == 1: card_code = "00"+card_code
        if len(card_code) == 2: card_code = "0"+card_code

        thumb_path = download_path + "/" + card_code + ".thumb.png"
        full_size_path = thumb_path.replace(".thumb","")
    
    if(img_type == "logo"):
        full_size_path = download_path + "/" + img_name[6] + ".png"

    #salva la thumb in memoria solo se non esiste
    """if thumb_path != "" and not os.path.exists(thumb_path):
        img = requests.get(url, stream=True)

        with open(thumb_path, "wb") as downloaded_img:
            downloaded_img.write(img.content)
            downloaded_img.close()"""

    #salva la full size in memoria solo se non esiste
    if not os.path.exists(full_size_path):
        img = requests.get(url.replace(".thumb",""), stream=True)

        with open(full_size_path, "wb") as downloaded_img:
            downloaded_img.write(img.content)
            downloaded_img.close()

    if(img_type == "card"):
        print(f"Downloaded {full_size_path}")
        return thumb_path
    
    if(img_type == "logo"):
        return full_size_path

#classe necessaria per il thread
class Search (Thread):
    
   def __init__(self, set_name, subsets_list, local_series_id):
      Thread.__init__(self)
      self.set_name = set_name
      self.subsets_list = subsets_list
      self.id = local_series_id

   def run(self):

        for i, subseries in enumerate(self.subsets_list):
            
            #creazione cartella immagini dedicata per ogni subset
            try:
                download_path = os.path.join(card_img_folder_path, subseries["id"].replace(" / "," ").replace(" ","_").replace(".","")) #replace per fix di un'estensione e per fix spazi linux
                os.mkdir(download_path)
                print("New folder for image storing created for " + subseries["name"]) 
            except FileExistsError:
                print("Image folder already exists for " + subseries["name"])
 
            sub_url = subseries["link"]
            print("[SYSTEM] : Downloading\t" + self.set_name + "\t(" + str(i+1) + "/" + str(len(self.subsets_list)) + ")\t " + subseries["name"])
            web = requests.get(sub_url)
            html = BeautifulSoup(web.content, 'html.parser')

            #variabile usata per capire quante carte normali e segrete ci sono
            cards = html.find(class_="cards").getText().replace("\n","").replace("Cards","").replace("Secret","").replace("+"," ")
            cards = re.split(" ",cards)
 
            #se non ci sono carte segrete gestisce l'eccezione
            try: 
                cards_number = cards[0].lstrip('0') #lstrip serve per togliere gli eventuali zeri all'inizio
                secret_number = cards[1].lstrip('0')
            except IndexError:
                secret_number=0
            
            #lista nomi
            cards_data = html.find_all("div", class_="card")
 
            subset_card_list=[] #lista delle carte del subset
 
            for card in cards_data:
                details = card.find(class_="plaque").getText() #memorizza i dettagli della carta in una sola stringa

                if "#" in details: #se c'è # la carta ha un codice
                    details = details.replace("#","").replace("-","")
                    details = re.split("  ",details)

                    cod = details[0].rjust(3,'0')+"/"+cards_number.rjust(3,'0')
                    name = details[1]
                else:
                    cod = "" #se la carta non ha codice allora memorizza una stringa vuota
                    name = details

                img = card.find("img") #prende link immagine se esiste
                if img != None:
                    img_src = img["data-src"]
                else:
                    img_src = ""

                img_link = img_download(img_src, download_path)
                    
                #metodo momentaneo per vedere se una carta è SR
                secret_rare = False

                if "/" in cod:
                    cod_splitted = re.split("/",cod)
                    if cod_splitted[0] > cod_splitted[1]:
                        secret_rare = True
                
                #salvataggio sia percorsi relativi che assoluti 
                data_dict= {"id" : subseries["id"] + cod.replace("/",""),
                            "name_EN" : name,
                            "cod" : cod,
                            "secret_rare" : secret_rare,
                            "standard_img_abs_path" : img_link.replace(".thumb",""),
                            "thumb_img_abs_path" : img_link,
                            "standard_img_rel_path" : "/" + os.path.relpath(img_link.replace(".thumb",""), img_folder_path),
                            "thumb_img_rel_path" : "/" + os.path.relpath(img_link, img_folder_path)}

                subset_card_list.append(data_dict)
 
            #aggiunge i dati delle carte ai dati principali
            sets_data[self.id]["subsets_list"][i]["cards_number"]=int(cards_number)
            sets_data[self.id]["subsets_list"][i]["secret_cards_number"]=secret_number
            sets_data[self.id]["subsets_list"][i]["cards_list"]=subset_card_list
 
            del sets_data[self.id]["subsets_list"][i]["link"]
 
        print("[SYSTEM] : \033[0;32mCompleted\033[0;0m\t" + self.set_name)

#funzione che prende nomi di set e subsets              
def set_name():
    #request alla pagina
    print("[SYSTEM] : Starting")
    web = requests.get(source_url)
    html = BeautifulSoup(web.content, 'html.parser')

    sets_list = html.find_all(class_="set")
    subsets_list = html.find_all(class_="buttonlisting")

    for i,set in enumerate(sets_list):

        if not set.getText() == 'Scarlet & Violet Series':
            continue

        print("[SYSTEM] : Found\t" + set.getText())

        subsets_name_list = subsets_list[i].find_all(class_="button") #trova i nomi di tutti i subset

        subsets_data=[] #contiene i dict dei subsets

        for subset in subsets_name_list:
            #organizza i dati in un dict

            #download logo immagine
            img_src = subset.find("img").get("src")
            img_link = img_download(img_src, logo_folder_path, "logo")

            subset_data_dict = {
                                "id" : subset.get("name"),
                                "name" : subset.getText(),
                                "link" : source_url.replace("/sets","")+subset.get("href"),
                                "standard_logo_abs_path" : img_link,
                                "standard_logo_rel_path" : "/" + os.path.relpath(img_link, img_folder_path),
                                "scraped" : False
                            }
            subsets_data.append(subset_data_dict)

        #organizza i dati in un dict e divide le sottoserie per serie principali
        set_data_dict = {
                            "set_name" : set.getText(),
                            "subsets_list" : subsets_data
                        }

        sets_data.append(set_data_dict)

if __name__ == '__main__':

    folder_setup()
    
    set_name()
    
    #parte dedicata ai threads
    threads=[]

    #scorre la lista data per ricavare le informazioni sulle carte contenute nei singoli subset
    for i,set in enumerate(sets_data):
        if sets_data[i]["set_name"] == "Scarlet & Violet Series": #messo per far scaricare solo espansioni di scarlatto e violetto
            threads.append(Search(sets_data[i]["set_name"],sets_data[i]["subsets_list"],i))

    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()

    #scrive un file json buttandoci tutto il contenuto di data
    with open(dest_file,"w",encoding="utf-8") as f:
        json.dump(sets_data,f,indent=4,ensure_ascii=False)
        f.close()

    print("Data updated")
