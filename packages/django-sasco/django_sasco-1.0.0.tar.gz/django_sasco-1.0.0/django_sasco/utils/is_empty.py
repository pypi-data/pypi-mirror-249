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
# Funcionalidades del módulo (funciones "públicas")
# ------------------------------------------------------------------------------

def is_empty(var, key=None):
    """
    Indica si una variable está "vacía", siguiendo reglas específicas para diferentes tipos de datos.
        - diccionarios: diccionario vacio (sin llave), llave no existe o está vacía la llave
        - listas: largo 0
        - tuplas: largo 0
        - conjuntos: largo 0
        - strings: valor '0', '0.0' o ''
        - enteros: valor 0
        - flotantes: valor 0
        - booleanos: valor False

    Args:
        var: La variable a verificar.
        key: La clave específica a verificar en un diccionario (opcional).

    Returns:
        bool: True si la variable está vacía según las reglas definidas.
    """

    # si la variable es None no se valida el resto porque es vacía por defecto
    if var is None:
        return True

    # diccionarios
    if isinstance(var, dict):
        # si no hay una llave específica, se revisa que el diccionario tenga algo
        if key is None:
            return len(var) == 0
        # buscar el valor final de la variable según la llave definida
        for k in key.split('.'):
            if k not in var:
                return True
            var = var[k]
        # la llave existe en el diccionario, hay que ver si tiene un valor no vacio
        return is_empty(var)

    # listas, tuplas y conjuntos
    if isinstance(var, list) or isinstance(var, tuple) or isinstance(var, set):
        return len(var) == 0

    # strings
    if isinstance(var, str):
        return var in ['0', '0.0', '']

    # enteros y flotantes
    if isinstance(var, (int, float)):
        return var == 0

    # booleanos
    if isinstance(var, bool):
        return not var

    # tipo de dato no soportado para validar si es vacío
    raise AttributeError('Tipo de dato no soportado por is_empty(): ' + str(type(var)))

# ------------------------------------------------------------------------------
# Casos de prueba
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    # Casos básicos
    assert is_empty(None) == True
    assert is_empty('') == True
    assert is_empty('0') == True
    assert is_empty('0.0') == True
    assert is_empty(0) == True
    assert is_empty(0.0) == True
    assert is_empty(False) == True
    assert is_empty({}) == True
    assert is_empty([]) == True
    assert is_empty(()) == True
    assert is_empty(set()) == True

    # Casos no vacíos
    assert is_empty('1') == False
    assert is_empty('texto') == False
    assert is_empty(1) == False
    assert is_empty(1.1) == False
    assert is_empty(True) == False
    assert is_empty({'a': 1}) == False
    assert is_empty([1, 2, 3]) == False
    assert is_empty((1, 2, 3)) == False
    assert is_empty({1, 2, 3}) == False

    # Diccionarios con claves anidadas
    assert is_empty({"a": {"b": 0}}, "a.b") == True
    assert is_empty({"a": {"b": 1}}, "a.b") == False
    assert is_empty({"a": {"b": {"c": None}}}, "a.b.c") == True
    assert is_empty({"a": {"b": {"c": "valor"}}}, "a.b.c") == False

    # Diccionarios con claves que no existen
    assert is_empty({"a": {"b": 1}}, "a.c") == True
    assert is_empty({"a": {}}, "a.b") == True

    print("Todos los casos de prueba pasaron.")
