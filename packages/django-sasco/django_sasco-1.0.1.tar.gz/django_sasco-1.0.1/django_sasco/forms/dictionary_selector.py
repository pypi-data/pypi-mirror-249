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


from django import forms

from abc import ABC

from ..utils.dictionary_selector import selector


# clase para un formulario que trabaja con datos en un diccionario mediante el selector
class SelectorForm(forms.Form):

    # constructor para poder cargar los datos iniciales del formulario desde el
    # diccionario que tiene los datos de manera estructurada
    def __init__(self, data, values = {}):
        if values != {}:
            super().__init__(data = values)
        else:
            super().__init__()
        for field in self.fields:
            self.fields[field].initial = selector(data, self.fields[field].selector)

    # método para obtener un diccionario con los datos del formulario de manera estructurada
    def get_data(self):
        data = {}
        for field in self.fields:
            selector(
                dictionary = data,
                id = self.fields[field].selector,
                value = self.fields[field].get_value(self.cleaned_data[field]),
                force_write = True
            )
        return data

# campo base para otros campos de un formulario SelectorForm
class SelectorField(ABC):
    selector = None

    def __init__(self, *args, **kwargs):
        self.selector = kwargs.pop('selector', None)
        if 'required' not in kwargs:
            kwargs['required'] = False
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 100
        super().__init__(*args, **kwargs)

    def get_value(self, value):
        python_value = self.to_python(value)
        # si es string y está vacío se entrega None, esto porque los datos que el
        # selector guarda no considera datos vacíos en los strings (sólo nulos)
        if isinstance(python_value, str) and python_value == '':
            return None
        # se entrega el valor de python
        return python_value

# campo de texto para el formulario SelectorForm
class SelectorCharField(SelectorField, forms.CharField):
    pass

# campo de correo electrónico para el formulario SelectorForm
class SelectorEmailField(SelectorField, forms.EmailField):
    pass

# campo que valida con una expresión regular para el formulario SelectorForm
class SelectorRegexField(SelectorField, forms.RegexField):
    pass
