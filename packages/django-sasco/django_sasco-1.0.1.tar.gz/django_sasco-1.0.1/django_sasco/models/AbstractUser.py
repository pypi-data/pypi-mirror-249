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

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser as DjangoAbstractUser
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _

from rest_framework.authtoken.models import Token

import hashlib
import os.path
from datetime import date
from smtplib import SMTPAuthenticationError
from webpush import send_user_notification

from .AbstractModel import AbstractModel
from ..exceptions import AppException

class AbstractUser(DjangoAbstractUser, AbstractModel):

    email = models.EmailField(
        max_length = 254,
        unique = True,
        verbose_name = _('Correo electrónico'),
    )

    class Meta:
        abstract = True
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
        ordering = ('-date_joined',)

    def __str__(self):
	    return self.first_name + ' ' + self.last_name + ' (' + self.username + ')'

    @property
    def token(self):
        try:
            return Token.objects.filter(user = self).get()
        except ObjectDoesNotExist:
            return None

    @token.setter
    def token(self, value):
        if value is True:
            if Token.objects.filter(user = self).exists():
                Token.objects.filter(user = self).delete()
            return Token.objects.create(user = self)
        else:
            del self.token

    @token.deleter
    def token(self):
        if Token.objects.filter(user = self).exists():
            Token.objects.filter(user = self).delete()

    @property
    def email_md5(self):
        return hashlib.md5(self.email.encode('utf-8')).hexdigest()

    @property
    def gravatar_url(self):
        return 'https://gravatar.com/avatar/' + self.email_md5

    @property
    def hash(self):
        key = str(settings.SECRET_KEY) + str(self.id) + str(self.username) + str(date.today())
        key_sha = hashlib.sha256(key.encode('utf-8')).hexdigest()
        key_md5 = hashlib.md5(key_sha.encode('utf-8')).hexdigest()
        return key_md5

    @property
    def in_support_team(self, support_team = 'soporte'):
        # TODO: optimizar property
        if self.groups.filter(name=support_team).exists():
            return True
        return self.groups.filter(name='support').exists()

    # envíar un correo electrónico que hace uso de una plantilla
    def send_email(self, subject, message=None, html_message=None, reply_to=None, attachments = [], template='default', **kwargs):
        # preparar mensajes a partir de las plantillas de correo
        if message is not None:
            message = str(message)
        if html_message is None and message is not None:
            html_message = '<p>' + message.replace("\n", '</p><p>') + '</p>'
        variables = {
            'username': self.username,
            'full_name': self.get_full_name(),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'anio': date.today().year,
            'message': message,
            'html_message': html_message,
        }
        txt = render_to_string('emails/' + template + '.txt', variables) if message is not None else None
        html = render_to_string('emails/' + template + '.html', variables) if html_message is not None else None
        # crear mensaje
        email = EmailMultiAlternatives()
        email.from_email = str(settings.DEFAULT_FROM_EMAIL)
        if reply_to is not None:
            email.reply_to = [reply_to]
        email.to = [self.email]
        email.subject = str(settings.EMAIL_SUBJECT_PREFIX) + ' ' + str(subject)
        if txt is not None:
            email.body = txt
        if html is not None:
            email.attach_alternative(html, 'text/html')
        mimetypes = {
            'pdf': 'application/pdf',
            'csv': 'text/csv',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        }
        for attachment in attachments:
            extension = os.path.splitext(attachment[0])[1]
            mimetype = attachment[2] if len(attachment) == 3 else (mimetypes[extension] if extension in mimetypes else None)
            email.attach(attachment[0], attachment[1], mimetype)
        try:
            return email.send()
        except SMTPAuthenticationError as e:
            raise AppException(e.smtp_error.decode('utf-8'))

    # envíar una notificación push al usuario
    def send_notification(self, head, body, url = None, ttl = 60*60*24):
        payload = {
            'head': settings.EMAIL_SUBJECT_PREFIX + ' ' + str(head),
            'body': str(body),
            'icon': settings.WEBPUSH_SETTINGS['ICON'],
        }
        if url is not None:
            payload['url'] = str(settings.WEBPUSH_SETTINGS['URL']) + str(url)
        send_user_notification(user = self, payload = payload, ttl = ttl)
