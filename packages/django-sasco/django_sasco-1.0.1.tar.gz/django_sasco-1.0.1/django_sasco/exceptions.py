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

from rest_framework.exceptions import APIException


# excepción para los errores estándares de la aplicación
# esto es para no usar Exception, ya que es un error puesto que
# al usar Exception se captura todo lo que herede de Exception
class AppException(Exception):

    message = None

    def __init__(self, message, code=None, params=None):
        self.message = str(message)
        super().__init__(message, code, params)

    def __str__(self):
        return self.message

# excepción para los errores de la API
class ApiException(APIException):
    # Antes se usaba el error 520, pero da problemas con el balanceador de carga en AWS
    # 520: Web Server Returned an Unknown Error (by Cloudflare)
    # 400: is the generic client-side error status, used when no other 4xx error code is appropriate.
    # Errors can be like malformed request syntax, invalid request message parameters, or deceptive request routing etc.
    # The client SHOULD NOT repeat the request without modifications.
    status_code = 400 # Bad Request
