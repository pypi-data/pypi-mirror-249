# -*- coding: utf-8 -*-

"""
django-sasco: Aplicación Base de SASCO SpA para el framework Django
Copyright (C) SASCO SpA (https://sasco.cl)

Este programa es software libre: usted puede redistribuirlo y/o modificarlo
bajo los términos de la GNU Lesser General Public License (LGPL) publicada
por la Fundación para el Software Libre, ya sea la versión 3 de la Licencia,
o (a su elección) cualquier versión posterior de la misma.

Este programa se distribuye con la esperanza de que sea útil, pero SIN
GARANTÍA ALGUNA; ni siquiera la garantía implícita MERCANTIL o de APTITUD
PARA UN PROPÓSITO DETERMINADO. Consulte los detalles de la GNU Lesser General
Public License (LGPL) para obtener una información más detallada.

Debería haber recibido una copia de la GNU Lesser General Public License
(LGPL) junto a este programa. En caso contrario, consulte
<http://www.gnu.org/licenses/lgpl.html>.
"""

from django.db import models, connection


# modelo abstracto con métodos estáticos para hacer consultas directamente a la
# base de datos, sin usar el ORM de django
class AbstractModel(models.Model):

    class Meta:
        abstract = True

    @staticmethod
    def run_query(query, params = {}) :
        """
            Método para ejecutar: INSERT, UPDATE o DELETE (pero no SELECT directamente)
            Args:
                query (:string): Cadena que recibe la accion sql a realizar
                param (list): Contiene los parametros a ingresar en la consulta sql.
            Return: cursor con la consulta SQL ejecutada
        """
        with connection.cursor() as cursor:
            if not bool(params) :
                cursor.execute(query)
            else :
                cursor.execute(query, params)
            return cursor

    @staticmethod
    def get_table(query, params = {}) :
        """
            Método que ejecuta un SELECT y devuelve una matriz de N filas y M columnas
            Args:
                query (:string): Cadena que recibe la accion sql a realizar
                param (dict): Contiene los parametros a ingresar en la consulta sql.
            Return: [{}, {}] -> lista de "objetos" (diccionarios)
        """
        with connection.cursor() as cursor:
            if not bool(params) :
                cursor.execute(query)
            else :
                cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

    @staticmethod
    def get_row(query, params = {}) :
        """
            Método que ejecuta un SELECT y devuelve una matriz de 1 fila y M columnas
            Args:
                query (:string): Cadena que recibe la accion sql a realizar
                param (dict): Contiene los parametros a ingresar en la consulta sql.
            Return: {} -> un "objeto" (diccionario)
        """
        with connection.cursor() as cursor:
            if not bool(params) :
                cursor.execute(query)
            else :
                cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, cursor.fetchone()))

    @staticmethod
    def get_col(query, params = {}) :
        """
            Método que ejecuta un SELECT y devuelve una matriz de N filas y 1 columna
            Args:
                query (:string): Cadena que recibe la accion sql a realizar
                param (dict): Contiene los parametros a ingresar en la consulta sql.
            Return: [''] -> lista de escalares
        """
        with connection.cursor() as cursor:
            if not bool(params) :
                cursor.execute(query)
            else :
                cursor.execute(query, params)
            columns = [col[0] for col in cursor.fetchall()]
            return columns

    @staticmethod
    def get_value(query, params = {}) :
        """
            Método que ejecuta un SELECT y devuelve una matriz de 1 fila y 1 columna
            Args:
                query (:string): Cadena que recibe la accion sql a realizar
                param (dict): Contiene los parametros a ingresar en la consulta sql.
            Return: '' -> un escalar
        """
        with connection.cursor() as cursor:
            if not bool(params) :
                cursor.execute(query)
            else :
                cursor.execute(query, params)
            value = cursor.fetchone()
            return value[0]

    @staticmethod
    def get_table_generator(query, params = {}) :
        """
            Método que ejecuta un SELECT y devuelve un generador para una matriz de N filas y M columnas
            Args:
                query (:string): Cadena que recibe la accion sql a realizar
                param (dict): Contiene los parametros a ingresar en la consulta sql.
            Return: yield {} -> genera un "objeto" (diccionario)
        """
        with connection.cursor() as cursor:
            if not bool(params) :
                cursor.execute(query)
            else :
                cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            table = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
            for row in table :
                yield row

    @staticmethod
    def get_col_generator(query, params = {}) :
        """
            Método que ejecuta un SELECT y devuelve un generador para una matriz de N filas y 1 columna
            Args:
                query (:string): Cadena que recibe la accion sql a realizar
                param (dict): Contiene los parametros a ingresar en la consulta sql.
            Return: yield '' -> genera un escalar
        """
        with connection.cursor() as cursor:
            if not bool(params) :
                cursor.execute(query)
            else :
                cursor.execute(query, params)
            columns = [col[0] for col in cursor.fetchall()]
            for col in columns :
                yield col
