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

from django import template
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter(name='alert', is_safe=True)
def alert(messages):
    icons = {
        'success': 'check-circle',
        'info': 'info-circle',
        'warning': 'exclamation-circle',
        'danger': 'exclamation-circle',
    }
    value = ''
    if messages:
        for message in messages:
            alert_type = 'danger' if message.tags == 'error' else message.tags
            value += '<div class="alert alert-' + alert_type + ' alert-dismissible fade show">'
            value += '<i class="fas fa-' + icons[alert_type] + ' fa-fw"></i> '
            value += '<span>' + str(message) + '</span>'
            value += '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar"></button>'
            value += '</div>' + "\n"
    return mark_safe(value)
