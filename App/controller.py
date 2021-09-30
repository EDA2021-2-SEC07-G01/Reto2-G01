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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initCatalog(option):
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.initCatalog(option)
    return catalog

# Funciones para la carga de datos

def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadArtists(catalog)
    loadArtworks(catalog)

def loadArtists(catalog):
    """
    Carga los artistas del archivo y los agrega a la lista de artistas
    """
    artistsfile = cf.data_dir + 'Artists-utf8-small.csv'
    input_file = csv.DictReader(open(artistsfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)


def loadArtworks(catalog):
    """
    Carga todas las obras de arte del archivo y las agrega a la lista de obras
    """
    artworksfile = cf.data_dir + 'Artworks-utf8-small.csv'
    input_file = csv.DictReader(open(artworksfile, encoding='utf-8'))
    for artwork in input_file:
        model.addArtwork(catalog, artwork)

# Funciones de ordenamiento
def sortArtworks(sublist, sorting_method):
    return model.sortArtworks(sublist, sorting_method)

# Funciones de consulta sobre el catálogo

def artistDates(catalog, anio_inicial, anio_final):
    return model.artistDates(catalog, anio_inicial, anio_final)

def artworksDates(catalog, date_inicial, date_final):
    return model.artworksDates(catalog, date_inicial, date_final)

def artist_technique(catalog, artist_name):
    return model.artist_technique(catalog, artist_name)

def artworks_artistnationality(catalog):
    return model.artworks_artistnationality(catalog)

def InfoArtworksNationality(catalog, list):
    return model.InfoArtworksNationality(catalog, list)

def artworks_department(catalog, department):
    return model.artworks_department(catalog, department)

def Generate_sublist(catalog, sample):
    return model.Generate_sublist(catalog, sample)

def give_artists_byID(catalog, const_ids):
    return model.give_artists_byID(catalog, const_ids)

def most_used_technique(techniques_artworks):
    return model.most_used_technique(techniques_artworks)

def MediumDateMap(catalog, medium):
    return model.MediumDateMap(catalog, medium)

def sortMediumDates(list):
    return model.sortMediumDates(list)