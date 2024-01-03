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

@register.filter(name='as_vertical', is_safe=True)
def as_vertical(field):
    check_field(field)
    fix_margin = True if field.errors or field.help_text else False
    if field_type(field) in ('Select'):
        class_parent = '<div class="select-style-1">' if not fix_margin else '<div class="select-style-1" style="margin-bottom:0px">'
        is_select = True
    else:
        class_parent = '<div class="input-style-1">' if not fix_margin else '<div class="input-style-1" style="margin-bottom:0px">'
        is_select = False
    value = '<div>'
    value += class_parent
    value += '<label for="' + field.id_for_label + '">'
    value += str(field.label)
    if field.field.required:
        value += ' <span class="font-weight-bold text-danger">*</span> '
    value += '</label>'
    if is_select:
        value += '<div class="select-position">'
    if 'class' not in field.field.widget.attrs:
        field.field.widget.attrs['class'] = ''
    field.field.widget.attrs['class'] += 'p-2 bg-transparent form-control'
    if 'password' in str(field):
        value += '<div class="input-group">'
        value += str(field)
        value += '<a class="input-group-text" style="cursor:pointer;text-decoration:none" onclick="Form.showPassword(this)">'
        value += '<i class="fa-regular fa-eye fa-fw"></i>'
        value += '</a>'
        value += '<a class="input-group-text" style="cursor:pointer;text-decoration:none" onclick="__.copy(this.parentNode.querySelector(`input`).value)">'
        value += '<i class="fas fa-copy fa-fw"></i>'
        value += '</a>'
        value += '</div>'
    else:
        value += str(field)
    if is_select:
        value += '</div>'
    value += '</div>'
    if fix_margin:
        value += '<div style="margin-bottom:30px">'
        if field.errors:
            for error in field.errors:
                value += '<p class="mt-1 mb-0 text-danger small"><i class="fa fa-times-circle fa-fw"></i> ' + error + '</p>'
        if field.help_text:
            value += '<p class="mt-1 mb-0 text-muted small"><i class="fa fa-info-circle fa-fw"></i> ' + str(field.help_text) + '</p>'
        value += '</div>'
    value += '</div>'
    return mark_safe(value)

@register.filter(name='as_horizontal', is_safe=True)
def as_horizontal(field, cols):
    check_field(field)
    form_control(field)
    value = ''
    value += '<div class="mb-3 row">'
    value += '<label for="' + field.id_for_label + '" class="col-md-' + str(cols) + ' col-form-label text-end">'
    if field.field.required:
        value += '<span class="font-weight-bold text-danger">*</span> '
    value += str(field.label)
    value += '</label>'
    value += '<div class="col-md-' + str(12-cols) + '">'
    if 'password' in str(field):
        value += '<div class="input-group">'
        value += str(field)
        value += '<a class="input-group-text" style="cursor:pointer;text-decoration:none" onclick="Form.showPassword(this)">'
        value += '<i class="fa-regular fa-eye fa-fw"></i>'
        value += '</a>'
        value += '<a class="input-group-text" style="cursor:pointer;text-decoration:none" onclick="__.copy(this.parentNode.querySelector(`input`).value)">'
        value += '<i class="fas fa-copy fa-fw"></i>'
        value += '</a>'
        value += '</div>'
    else:
        value += str(field)
    if field.errors:
        for error in field.errors:
            value += '<p class="mt-1 mb-0 text-danger small"><i class="fa fa-times-circle fa-fw"></i> ' + error + '</p>'
    if field.help_text:
        value += '<p class="mt-1 mb-0 text-muted small"><i class="fa fa-info-circle fa-fw"></i> ' + str(field.help_text) + '</p>'
    value += '</div>'
    value += '</div>'
    return mark_safe(value)

@register.filter(name='as_without_label')
def as_without_label(field):
    check_field(field)
    form_control(field)
    value = ''
    value += '<div class="mb-3 row">'
    value += '<div class="col-md-12">'
    value += '<label for="' + field.id_for_label + '" class="sr-only">' + str(field.label) + '</label>'
    if 'password' in str(field):
        value += '<div class="input-group">'
        value += str(field)
        value += '<a class="input-group-text" style="cursor:pointer;text-decoration:none" onclick="Form.showPassword(this)">'
        value += '<i class="fa-regular fa-eye fa-fw"></i>'
        value += '</a>'
        value += '<a class="input-group-text" style="cursor:pointer;text-decoration:none" onclick="__.copy(this.parentNode.querySelector(`input`).value)">'
        value += '<i class="fas fa-copy fa-fw"></i>'
        value += '</a>'
        value += '</div>'
    else:
        value += str(field)
    if field.errors:
        for error in field.errors:
            value += '<p class="mt-1 mb-0 text-danger small"><i class="fa fa-times-circle fa-fw"></i> ' + error + '</p>'
    if field.help_text:
        value += '<p class="mt-1 mb-0 text-muted small"><i class="fa fa-info-circle fa-fw"></i> ' + str(field.help_text) + '</p>'
    value += '</div>'
    value += '</div>'
    return mark_safe(value)

@register.filter(name='placeholder')
def placeholder(field, value):
    check_field(field)
    field.field.widget.attrs['placeholder'] = value
    return field

@register.filter(name='autofocus')
def autofocus(field):
    check_field(field)
    field.field.widget.attrs['autofocus'] = 'autofocus'
    return field

@register.filter(name='form_control')
def form_control(field, suffix = None):
    check_field(field)
    if 'class' not in field.field.widget.attrs or field.field.widget.attrs['class']=='':
        if field_type(field) in ('TextInput', 'NumberInput', 'EmailInput', 'URLInput', 'PasswordInput', 'Textarea', 'DateInput', 'DateTimeInput', 'TimeInput', 'Select'):
            field.field.widget.attrs['class'] = 'form-control'
            if field_type(field) in ('Select'):
                field.field.widget.attrs['class'] = 'form-control select2'
            if suffix:
                field.field.widget.attrs['class'] += ' form-control-'+suffix
    return field

@register.filter(name='field_type')
def field_type(field):
    check_field(field)
    return field.field.widget.__class__.__name__

def check_field(field):
    if field.__class__.__name__ != 'BoundField':
        raise Exception('No es posible usar el filtro en ' + field.__class__.__name__)
