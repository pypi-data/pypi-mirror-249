#!/usr/bin/python3
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
# ------------------------------------------------------------------------------
# Funcionalidades del módulo
# ------------------------------------------------------------------------------

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

from datetime import datetime
import os.path

from sasco_utils.datetime import period_previous, month_from_number


# método que envía un correo electrónico como si fuese este usuario a otro correo (no el del usuario)
def send_email_to(to, subject, message, reply_to = None, attachments = [], is_html = False, template = None, template_vars = {}):
    """
        Método que envía un correo electrónico como si fuese este usuario a otro correo (no el del usuario)

        Args:
            subject (str):
            message (str):
            reply_to (str):
            attachments (binary);
            is_html (bool):
            template (str):
            template_vars (dict):

        Returns:
            int:
    """
    # preparar datos que se usarán para el correo
    if not isinstance(to, list):
        to = list(to) if isinstance(to, tuple) else [to]
    to = list(map(lambda e: str(e).strip(), to))
    subject = str(subject).strip()
    message = str(message).strip()
    if reply_to is None:
        reply_to = settings.DEFAULT_FROM_EMAIL
    # si el mensaje va en una plantilla se debe armar el mensaje pasado dentro de la plantilla
    if template is not None:
        today = datetime.now()
        template_vars = {**{
            # datos originales del correo
            'to': to,
            'subject': subject,
            'message': message if is_html or not template.endswith('.html') else '<p>' + message.replace("\n", '</p><p>') + '</p>',
            'reply_to': reply_to,
            # datos para la plantilla
            'title': subject,
            'url': settings.HOSTNAME,
            'today_date': month_from_number(today.month) + ' ' + str(today.year),
            'today_year': today.year,
        }, **template_vars}
        message_html = render_to_string(template, template_vars)
    # si el mensaje es HTML pero sin plantilla se copia directamente el mensaje original como mensaje HTML
    elif is_html:
        message_html = message
    # si el mensaje no es HTML, no se usará esa alternativa
    else:
        message_html = None
    # crear mensaje de correo
    mail = EmailMultiAlternatives()
    mail.from_email = settings.DEFAULT_FROM_EMAIL
    mail.reply_to = [reply_to]
    mail.to = to
    mail.subject = subject
    mail.body = message
    if message_html is not None:
        mail.attach_alternative(message_html, 'text/html')
    # agregar adjuntos
    mimetypes = {
        'pdf': 'application/pdf',
        'csv': 'text/csv',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'png': 'image/png',
    }
    for attachment in attachments:
        extension = os.path.splitext(attachment[0])[1]
        mimetype = attachment[2] if len(attachment) == 3 else (mimetypes[extension] if extension in mimetypes else None)
        mail.attach(attachment[0], attachment[1], mimetype)
    # enviar correo electrónico
    return mail.send()