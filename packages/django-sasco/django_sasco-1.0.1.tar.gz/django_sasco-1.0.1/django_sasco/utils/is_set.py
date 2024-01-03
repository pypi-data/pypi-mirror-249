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
from django.utils.translation import gettext_lazy as _


# verificar si la llave de un diccionario existe
def is_set(var, keys = None):
    if not isinstance(var, dict):
        raise AttributeError(_('No se especificó un diccionario'))
    if keys is None:
        raise AttributeError(_('Se espera que se especifiquen las llaves del diccionario'))
    array_keys = keys.split('.')
    if len(array_keys) == 0:
        raise AttributeError(_('Estructura de las llaves ingresada es incorrecta'))
    var_search = var
    for key in array_keys:
        try:
            var_search = var_search[key]
            if var_search is None:
                return False
        except KeyError:
            return False
    return True
# ------------------------------------------------------------------------------
# TODO Caso de prueba
# ------------------------------------------------------------------------------
#
# TODO resultado de la ejecución del caso de prueba
#
