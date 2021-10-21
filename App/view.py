"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
import ipdb
from tabulate import tabulate
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from collections import OrderedDict
assert cf

default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1 - Cargar información en el catálogo")
    print("2 - Listar cronológicamente los artistas")
    print("3 - Listar cronológicamente las adquisiciones")
    print("4 - Clasificar las obras de un artista por técnica")
    print("5 - Clasificar la obra por la nacionalidad de sus creadores")
    print("6 - Transportar obras de un departamento")
    print("0 - Salir")

def initCatalog(option): # the option is for selecting the datastructure
    """
    Inicializa el catalogo de obras de arte
    """
    return controller.initCatalog(option)

def loadData(catalog):
    """
    Carga las obras de arte en la estructura de datos
    """
    controller.loadData(catalog)

def ArtistSize(catalog):
    list_artists = catalog['artists']
    print("\nEl número total de artistas es: "+str(lt.size(list_artists)))

def ArtworkSize(catalog):
    list_artworks = catalog['artworks']
    print("El número total de obras de arte es: "+str(lt.size(list_artworks)))

def artistDates(catalog, anio_inicial, anio_final):
    return controller.artistDates(catalog, anio_inicial, anio_final)

def artworksDates(catalog, date_inicial, date_final):
    return controller.artworksDates(catalog, date_inicial, date_final)

def artist_technique(catalog, artist_name):
    return controller.artist_technique(catalog, artist_name)

def artworks_artistnationality(catalog):
    return controller.artworks_artistnationality(catalog)

def artworks_department(catalog, department):
    return controller.artworks_department(catalog, department)

def most_used_technique(techniques_artworks):
    return controller.most_used_technique(techniques_artworks)

def artist_nationality(catalog):
    return controller.artist_nationality(catalog)

def topNationalityArtist(catalog, nationality):
    return controller.topNationalityArtist(catalog, nationality)

# PRINT Functions

def printResultsArtworks(ord_list, sample = 3):
    size = lt.size(ord_list)
    if size > sample:
        print("Las primeras ", sample, "obras de arte ordenadas son: ")
        i = 1
        j = -2
        while i <= sample:
            artwork = lt.getElement(ord_list, i)
            const_ids = artwork["ConstituentID"]
            artists = controller.give_artists_byID(catalog, const_ids)
            print("Title: " + artwork["Title"] + ", Date: " + artwork["DateAcquired"] + ", Medio: " + artwork["Medium"] + ", Dimensiones: " + artwork["Dimensions"])
            print("Los artistas involucrados fueron: ", (artists['elements']))
            i += 1
        print("----------------------------------------------------------------------------------")
        print("Las últimas ", sample, "obras de arte ordenadas son: ")
        while j+2 < sample:
            artwork = lt.getElement(ord_list, size + j )
            const_ids = artwork["ConstituentID"]
            artists = controller.give_artists_byID(catalog, const_ids)
            print("Title: " + artwork["Title"] + ", Date: " + artwork["DateAcquired"] + ", Medio: " + artwork["Medium"] + ", Dimensiones: " + artwork["Dimensions"])
            print("Los artistas involucrados fueron: ", (artists['elements']))
            j += 1

def printResultsArtists(ord_list, sample = 3):
    size = lt.size(ord_list)
    if size > sample:
        print("Los primeros ", sample, "artistas en el rango dado son: ")
        i = 1
        j = -2
        while i <= sample:
            artist = lt.getElement(ord_list, i)
            print("Nombre: " + artist["name"] + ", Nacimiento: " + artist["birth_date"] + ", Fallecimiento: " + artist["end_date"] + ", Nacionalidad: " + artist["nationality"] + ", Género: " + artist["gender"])
            i += 1
        print("----------------------------------------------------------------------------------")
        print("Los últimos ", sample, "artistas en el rango dado son: ")
        while j+2 < sample:
            artist = lt.getElement(ord_list, size + j )
            print("Nombre: " + artist["name"] + ", Nacimiento: " + artist["birth_date"] + ", Fallecimiento: " + artist["end_date"] + ", Nacionalidad: " + artist["nationality"] + ", Género: " + artist["gender"])
            j += 1

def printResultsArtworksNationality(artworks_nationality):
    print("The TOP 10 Countries in the MoMA are:")
    headers = ["Nationality", "ArtWorks"]
    table1 = []
    contador = 0
    for element in artworks_nationality:
        x, y = element
        contador += 1
        if contador == 11:
            break 
        table1.append([x, y])
    print(tabulate(table1,headers, tablefmt="grid"))

def printResultsNationalityInfo(names, artworks_list, sample=3):
    size = lt.size(artworks_list)
    if size > sample:
        print("Las primeras ", sample, "obras del TOP 1 nacionalidad son: ")
        i = 1
        j = 0
        while i <= sample:
            artworks = lt.getElement(artworks_list, i)
            print("Título: "+ artworks['Title']+", Artistas: " + lt.getElement(names, i)['first']['info']+", Fecha: "+ artworks['Date']+", Medio: "+artworks['Medium']+ ", Dimensiones: "+artworks['Dimensions'])
            i += 1
        print("----------------------------------------------------------------------------------")
        print("Las últimas ", sample, "tres obras del TOP¨1 de nacionalidad son: ")
        while j < sample:
            artworks = lt.getElement(artworks_list, size - j )
            print("Título: "+ artworks['Title']+", Artistas: " + lt.getElement(names, j)['first']['info']+", Fecha: "+ artworks['Date']+", Medio: "+artworks['Medium']+ ", Dimensiones: "+artworks['Dimensions'])
            j += 1

def print_artworks_technique(techniques_dic, most_used_tech):
        size = lt.size(mp.get(techniques_dic,most_used_tech)['value'])
        if size < 3:
            print("No hay suficientes obras para imprimir")
        else:
            print("Las primeras ", str(3), "obras de la técnica son: ")
            i = 1
            j = -2
            while i <= 3:
                artwork = lt.getElement(mp.get(techniques_dic,most_used_tech)['value'], i)
                print("Título: " + artwork["Title"] + ", Fecha: " + artwork["Date"] + ", Medio: " + artwork["Medium"] + ", Dimensiones: " + artwork["Dimensions"])
                i += 1
            print("----------------------------------------------------------------------------------")
            print("Las últimas ", str(3), "obras de la técnica son: ")
            while j+2 < 3:
                artwork = lt.getElement(mp.get(techniques_dic,most_used_tech)['value'], size + j)
                print("Título: " + artwork["Title"] + ", Fecha: " + artwork["Date"] + ", Medio: " + artwork["Medium"] + ", Dimensiones: " + artwork["Dimensions"])
                j += 1

def print5expensive(artworks_price, sample=5):
    size = lt.size(artworks_price)
    if size > sample:
        print("Las " + str(sample) + " obras más caras son: ")
        i = 1
        while i <= sample:
            artwork = lt.getElement(artworks_price, i)
            print("Title: " + artwork["Title"] + ", Date: " + artwork["Date"] + ", Medio: " + artwork["Medium"] + ", Dimensiones: " + artwork["Dimensions"])
            i += 1

def print5oldest(artworks_date, sample=5):
    size = lt.size(artworks_date)
    if size > sample:
        print("Las " + str(sample) + " obras más antiguas son: ")
        i = 0
        while i < sample:
            artwork = lt.getElement(artworks_date, size - i)
            print("Title: " + artwork["Title"] + ", Date: " + artwork["Date"] + ", Medio: " + artwork["Medium"] + ", Dimensiones: " + artwork["Dimensions"])
            i += 1

def printMediumOldest(list, n):
    try:
        print("Las "+str(n)+" obras más antiguas son: ")
        headers = ["Artwork Title", "Date", "Medium"]
        table = []
        sublist = lt.subList(list, 1, n)
        print(sublist)
        for artwork in lt.iterator(sublist):
            table.append([artwork['Title'], artwork['Date'], artwork['Medium']])
        print(tabulate(table,headers, tablefmt="grid"))
    except:
        print("El tamaño de elementos supera el tamaño de la lista de las obras.")



catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog(option=1)
        loadData(catalog)
        ArtistSize(catalog)
        ArtworkSize(catalog)

    elif int(inputs[0]) == 2:
        anio_inicial = int(input("Ingrese el año inicial: "))
        anio_final = int(input("Ingrese el año final: "))
        organized = artistDates(catalog, anio_inicial, anio_final)
        print("El número total de artistas para el rango dado es: " + str(lt.size(organized)))
        printResultsArtists(organized, sample=3)

    elif int(inputs[0]) == 3:
        date_inicial = input('Ingrese la fecha inicial de adquisición en el formato AAAA-MM-DD: ')
        date_final = input('Ingrese la fecha final de adquisición en el formato AAAA-MM-DD: ')
        organized, contador = artworksDates(catalog, date_inicial, date_final)
        print("El número total de obras en el rango cronológico es: " + str(lt.size(organized)))
        print("El número total de obras adquiridas por compra es: " + str(contador))
        printResultsArtworks(organized, sample=3)

    elif int(inputs[0]) == 4:
        name_artist = input("Ingrese el nombre del artista para clasificar sus obras por técnica: ")
        contador, techniques, information = artist_technique(catalog, name_artist)
        print("El número total de obras para: " + name_artist + " son: " + str(contador))
        print("El número total de técnicas utilizadas por " + name_artist + " son: " + str(techniques))
        most_used_tech = most_used_technique(information)
        print("La técnica más utilizada por " + name_artist + "es: " + most_used_tech)
        print_artworks_technique(information, most_used_tech)

    elif int(inputs[0]) == 5:
        nationality, top, information = artist_nationality(catalog)
        names = topNationalityArtist(catalog, top)
        #print(names)
        #print(information)
        printResultsArtworksNationality(nationality)
        printResultsNationalityInfo(names, information)
        
    elif int(inputs[0]) == 6:
        department = input("Departamento del museo: ")
        artworks_price, artworks_date = artworks_department(catalog, department)
        print("El total de obras a transportar es: " + str(lt.size(artworks_price)))
        print5expensive(artworks_price)
        print("----------------------------------------------------------------------------------")
        print5oldest(artworks_date)

    else:
        sys.exit(0)
sys.exit(0)