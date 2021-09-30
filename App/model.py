"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures.arraylist import subList
from DISClib.Algorithms.Sorting import shellsort as shell
from DISClib.Algorithms.Sorting import insertionsort as insertion
from DISClib.Algorithms.Sorting import mergesort as merge 
from DISClib.Algorithms.Sorting import quicksort as quick
import operator
import datetime
import time
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def initCatalog(option):
    """
    Inicializa el catálogo de obras del MoMA. Crea una lista vacia para guardar
    todos los artistas y las obras de arte. Retorna el catalogo inicializado.
    """
    if option == 1:
        catalog = {'artists': None,
               'artworks': None,
               'Medium': None}
        catalog['artists'] = lt.newList(datastructure="SINGLE_LINKED") #Función de comparación
        catalog['artworks'] = lt.newList(datastructure="SINGLE_LINKED") #Función de comparación
        catalog['Medium'] = mp.newMap()
    return catalog

# Funciones para AGREGAR informacion al catalogo

def addArtist(catalog, artist):
    """
    Adiciona un artista a la lista de artistas
    """
    aux = newArtist(artist['DisplayName'], artist['BeginDate'], artist['EndDate'], artist['Nationality'], artist['Gender'], artist['ConstituentID'])
    lt.addLast(catalog['artists'], aux)

def addArtwork(catalog, artwork):
    """
    Adiciona una obra de arte a la lista de obras de arte
    """
    t = newArtwork(artwork['Title'], artwork['DateAcquired'], artwork['CreditLine'], artwork['ConstituentID'], artwork['Date'], artwork['Medium'], artwork['Dimensions'], artwork['Department'], 
    artwork['Depth (cm)'], artwork['Height (cm)'], artwork['Length (cm)'], artwork['Weight (kg)'], artwork['Width (cm)'], artwork['Seat Height (cm)'])
    lt.addLast(catalog['artworks'], t)

# Funciones para creacion de datos

def newArtist(name, birth_date, end_date, nationality, gender, const_id):
    """
    Esta estructura almancena los tags utilizados para marcar artistas.
    """
    artist = {'name': name, 'birth_date': birth_date, 'end_date': end_date, 'nationality': nationality, 'gender': gender, 'const_id': const_id}
    return artist

def newArtwork(name, date_acqu, credit, artist, date, medium, dimensions, department, depth, height, length, weight, width, seat_height):
    """
    Esta estructura almancena las obras de arte.
    """
    artwork = {'Title': name, 'DateAcquired':date_acqu, 'CreditLine':credit, 'ConstituentID': artist, 'Date': date, 'Medium': medium, 'Dimensions': dimensions, 'Department':department,
    'Depth':depth, 'Height': height, 'Length': length, 'Weight': weight, 'Width': width, 'Seat Heigth': seat_height}
    return artwork

# Funciones de CONSULTA

def MediumDateMap(catalog):
    for artwork in lt.iterator(catalog["artworks"]):
        artwork_medium = artwork["Medium"]
        if mp.contains(catalog['Medium'], artwork_medium) == False:
            medium_list = lt.newList(datastructure='SINGLE_LINKED')
            lt.addFirst(medium_list, artwork)
            mp.put(catalog['Medium'], artwork_medium, medium_list)
        else:
            medium_list = mp.get(catalog['Medium'], artwork_medium)['value']
            lt.addFirst(medium_list, artwork)
    return catalog

def MediumSpecificList(catalog, medium):
    medium_map = catalog['Medium']
    if mp.contains(medium_map, medium):
        medium_elements = mp.get(medium_map, medium)['value']
    return medium_elements

def give_artists_byID(catalog, const_ids):
    ids_list = const_ids[1:-1].split(",") # Since split is used, this is a native python list
    ids_nums = lt.newList("ARRAY_LIST")
    for i in ids_list: # Turning it into a DISClib list
        lt.addLast(ids_nums, i.strip()) 
    name_lists = lt.newList("ARRAY_LIST")
    for artist in lt.iterator(catalog["artists"]):
        if artist["const_id"].strip() in lt.iterator(ids_nums):
            lt.addLast(name_lists, artist['name'])
    return name_lists

def artistDates(catalog, anio_inicial, anio_final):
    artist_year_list = lt.newList(datastructure="ARRAY_LIST", cmpfunction= compareArtistsDates)
    #for artist in lt.iterator(catalog["artists"]["elements"]):
    for artist in lt.iterator(catalog["artists"]):
        try:
            if int(artist["birth_date"]) >= anio_inicial and int(artist["birth_date"]) <= anio_final:
                lt.addLast(artist_year_list, artist)
        except:
            pass
    sorted_list = sortArtistDates(artist_year_list)
    return sorted_list

def artworksDates(catalog, date_inicial, date_final):
    artworks_list = lt.newList(datastructure="ARRAY_LIST", cmpfunction= cmpArtworkByDateAcquired)
    contador = 0
    for artwork in lt.iterator(catalog["artworks"]):
        try:
            artwork_date = artwork["DateAcquired"].split("-")
            initial = date_inicial.split("-")
            final = date_final.split("-")
            if (datetime.datetime(int(artwork_date[0]), int(artwork_date[1]), int(artwork_date[2])) >= 
            (datetime.datetime(int(initial[0]), int(initial[1]), int(initial[2])))) and (datetime.datetime(int(artwork_date[0]), int(artwork_date[1]), int(artwork_date[2])) <= 
            (datetime.datetime(int(final[0]), int(final[1]), int(final[2])))):
                if "purchase" in artwork["CreditLine"].lower():
                    contador += 1
                lt.addLast(artworks_list, artwork)
        except:
            pass    
    sorted_list = sortArtworksDates(artworks_list)
    return sorted_list, contador

def artist_technique(catalog, artist_name):
    for artist in lt.iterator(catalog["artists"]):
        if artist["name"].strip().lower() == artist_name.lower():
            const_id = artist["const_id"]
            break # Se encontró el id del artista buscado
    contador = 0
    techniques_artworks = {}
    for artwork in lt.iterator(catalog["artworks"]):
        if const_id in (artwork["ConstituentID"][1:-1].split(",")):
            contador += 1
            if artwork["Medium"] not in techniques_artworks:
                artworks_list = lt.newList("ARRAY_LIST")
                lt.addLast(artworks_list, artwork) 
                techniques_artworks[artwork["Medium"]] = artworks_list
            else:
                artworks_list = techniques_artworks[artwork["Medium"]]
                lt.addLast(artworks_list, artwork) 
    return contador, techniques_artworks

def most_used_technique(techniques_artworks):
    most_used_tech = list(techniques_artworks.keys())[0]
    for tech in techniques_artworks.keys():
        if(lt.size(techniques_artworks[tech]) > lt.size(techniques_artworks[most_used_tech])):
            most_used_tech = tech
    return most_used_tech

def artworks_artistnationality(catalog):
    id_list = lt.newList(datastructure='ARRAY_LIST')
    for artwork in lt.iterator(catalog["artworks"]):
        id_artist = artwork["ConstituentID"][1:-1].split(",")
        for number in id_artist:
            lt.addLast(id_list, number.strip())
    nationality = {}
    for artist in lt.iterator(catalog["artists"]):
        for id_artist in lt.iterator(id_list):
            if id_artist == artist['const_id'].strip():
                artist_place = artist['nationality']
                if artist['nationality'] == "":
                    artist_place= "Nationality unknown"
                if not artist_place in nationality:
                    nationality[artist_place] = 1
                else:
                    nationality[artist_place] += 1
    sorted_dicc = sorted(nationality.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_dicc 

def InfoArtworksNationality(catalog, list):
    place, num = list[0]
    list_artist_id = lt.newList("ARRAY_LIST")
    list_artist_name = lt.newList("ARRAY_LIST")
    for artist in lt.iterator(catalog['artists']):
        if artist['nationality'] == place:
            lt.addLast(list_artist_id, artist['const_id'])
            lt.addLast(list_artist_name, artist['name'])
    artworks_list = lt.newList(datastructure='ARRAY_LIST')
    for artwork in lt.iterator(catalog["artworks"]):
        for id_artist in lt.iterator(list_artist_id):
            if id_artist in artwork["ConstituentID"]:
                lt.addLast(artworks_list, artwork)
    return list_artist_name, artworks_list

def artworks_department(catalog, department):
    artworks = lt.newList("ARRAY_LIST") # lista de las obras de un departamento dado
    for artwork in lt.iterator(catalog["artworks"]):
        if artwork["Department"] == department:
            artwork["Mayor_precio"] = 48
            if artwork['Weight'] == "":
                    artwork['Weight']= "0"
            precio_peso = (float(artwork['Weight'])*72)
            if (precio_peso > artwork['Mayor_precio']):
                artwork['Mayor_precio'] = precio_peso
            if artwork['Height'] == "" or artwork['Length'] == "": # Not enough information to calculate the price
                precio_dimension = 0 # It will take into account the 48 default price since it is higher   
            elif artwork['Depth'] != "" and artwork['Seat Heigth'] != "":
                precio_dimension = ((float(artwork['Depth'])*(float(artwork['Height'])+ float(artwork['Seat Heigth']))*float(artwork['Length'])))*(72/1000000) # m^3 a cm^3
            elif  artwork['Depth'] != "":
                precio_dimension = ((float(artwork['Depth'])*(float(artwork['Height']))*float(artwork['Length'])))*(72/1000000) # m^3 a cm^3
            elif  artwork['Seat Heigth'] != "":
                precio_dimension = ((float(artwork['Height']) + float(artwork['Seat Heigth']))*float(artwork['Length']))*(72/10000) # m^2 a cm^2            
            else:
                precio_dimension = ((float(artwork['Height']))*float(artwork['Length']))*(72/10000) # m^2 a cm^2            
            if (precio_dimension > artwork['Mayor_precio']):
                artwork['Mayor_precio'] = precio_dimension            
            lt.addLast(artworks, artwork)
    artworks_price = merge.sort(artworks, compareArtworByPrice)
    artworks_date = merge.sort(artworks, cmpArtworkByDate)
    return artworks_price, artworks_date

# Funciones de COMPARACIÓN

def compareArtistsDates(artist1, artist2):
    try:
        if int(artist1["birth_date"]) <= int(artist2["birth_date"]):
            return True
        else:
            return False
    except:
        pass

def compareArtworByPrice(artwork1, artwork2):
    try:
        if float(artwork1["Mayor_precio"]) >= float(artwork2["Mayor_precio"]):
            return True
        else:
            return False
    except:
        pass

def compareArtists(authorname1, author):
    if (authorname1.lower() in author['name'].lower()):
        return 0
    return -1

def cmpArtworkByDateAcquired(artwork1, artwork2): #Formato = año-mes-día
    """
    Devuelve verdadero (True) si el 'DateAcquired' de artwork1 es menor que el de artwork2
    Args:
    artwork1: informacion de la primera obra que incluye su valor 'DateAcquired'
    artwork2: informacion de la segunda obra que incluye su valor 'DateAcquired'
    """
    try:
        d1 = artwork1["DateAcquired"].split("-")
        d1 = [int(date) for date in d1]
        d2 = artwork2["DateAcquired"].split("-")
        d2 = [int(date) for date in d2]
        if (datetime.datetime(d1[0], d1[1], d1[2]) < datetime.datetime(d2[0], d2[1], d2[2])): #debido al formato
            return True
        else:
            return False
    except:
        pass


def cmpArtworkByDate(artwork1, artwork2): #Formato = año-mes-día
    """
    Devuelve verdadero (True) si el 'Date' de artwork1 es menor que el de artwork2
    Args:
    artwork1: informacion de la primera obra que incluye su valor 'Date'
    artwork2: informacion de la segunda obra que incluye su valor 'Date'
    """
    try:
        d1 = artwork1["Date"]
        d2 = artwork2["Date"]
        if (datetime.datetime(int(d1)) < datetime.datetime(int(d2))): #debido al formato AAAA
            return True
        else:
            return False
    except:
        pass

def cmpArtWorkMedium(artwork1, artwork2):
    d1 = artwork1['Date']
    d2 = artwork2['Date']
    return d1 < d2

# Funciones de ordenamiento

def sortArtistDates(list):
    return merge.sort(list, compareArtistsDates)

def sortArtworksDates(list):
    return merge.sort(list, cmpArtworkByDateAcquired)

def sortMediumDates(list):
    return merge.sort(list, cmpArtWorkMedium)

# ---
def Generate_sublist(catalog, sample):
    assert(sample <= lt.size(catalog['artworks'])), "Debe indicar un tamaño menor o igual a la cantidad de total de obras de arte"
    return lt.subList(catalog['artworks'],1,sample)

