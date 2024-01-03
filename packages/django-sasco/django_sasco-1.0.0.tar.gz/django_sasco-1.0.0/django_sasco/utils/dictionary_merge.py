#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# BillMySales: Pasarela de Facturación
# Copyright (C) SASCO SpA (https://sasco.cl)
#
# Este archivo está sujeto a los términos y condiciones definidos en
# el archivo 'LICENSE.md', el cual es parte de este paquete de código fuente.
#
# This file is subject to the terms and conditions defined in
# the file 'LICENSE.md', which is part of this source code package.
#

# ------------------------------------------------------------------------------
# Funcionalidades del módulo
# ------------------------------------------------------------------------------

# Dependencias de este módulo
import re # módulo de expresiones regulares


# Función que realiza que realiza un merge desde dictionary_b a dictionary_a
def merge(dictionary_a, dictionary_b, path=None):
    # merges b into a
    if path is None:
        path = []
    for key in dictionary_b:
        if key in dictionary_a:
            if isinstance(dictionary_a[key], dict) and isinstance(dictionary_b[key], dict):
                merge(dictionary_a[key], dictionary_b[key], path + [str(key)])
            elif dictionary_a[key] == dictionary_b[key]:
                pass # same leaf value
            else:
                dictionary_a[key] = dictionary_b[key]
        else:
            dictionary_a[key] = dictionary_b[key]
    return dictionary_a
# ------------------------------------------------------------------------------
# Caso de prueba
# ------------------------------------------------------------------------------

if __name__ == '__main__':
    # diccionario con datos para los casos de pruebas
    dictionary_a = {
        'otro': 1,
        'mas': {
            'mas2': {
                'mas3': {}
            }
        },
        'tipo': {
            'casa1': 1,
            'casa': ['1', '2'],
        },
        'mas': {}
    }
    dictionary_b = {
        'tipo': {
            'casa': ['3', '4']
        }
    }

    # ejecutar los casos de prueba y mostrar una tabla con los resultados
    print("==============")
    print('Diccionario A')
    print(dictionary_a)
    print("==============")
    print('Diccionario B')
    print(dictionary_b)
    print("==============")
    dictionary_merge = merge(dictionary_a, dictionary_b)
    print('Diccionario Merge')
    print(dictionary_merge)
    print("==============")

# resultado de la ejecución del caso de prueba de lectura
""""
==============
Diccionario A
{'otro': 1, 'mas': {}, 'tipo': {'casa1': 1, 'casa': ['1', '2']}}
==============
Diccionario B
{'tipo': {'casa': ['3', '4']}}
==============
Diccionario Merge
{'otro': 1, 'mas': {}, 'tipo': {'casa1': 1, 'casa': ['3', '4']}}
==============
"""