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


import base64
import re


# https://stackoverflow.com/a/9807138
def base64_decode(data, altchars = b'+/'):
    """Decode base64, padding being optional.
    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.
    """
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)
