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
# Dependencias de este módulo
# ------------------------------------------------------------------------------

# módulo de expresiones regulares
import re

# módulo para JSONPath
from jsonpath import jsonpath

# módulo para JMESPath
import jmespath

# ------------------------------------------------------------------------------
# Funcionalidades del módulo (funciones "públicas")
# ------------------------------------------------------------------------------

def dictionary_read_case_insensitive(dictionary, key):
    """
    Obtiene un valor de un diccionario sin considerar la diferencia entre mayúsculas y minúsculas en la clave.

    Args:
        dictionary (dict): El diccionario de donde leer.
        key (str): La clave a buscar, ignorando mayúsculas y minúsculas.

    Returns:
        El valor asociado con la clave en cualquier combinación de mayúsculas y minúsculas.
        Retorna None si la clave no se encuentra en el diccionario.
    """
    _dictionary = {k.lower(): v for k, v in dictionary.items()}
    _key = key.lower()
    return _dictionary.get(_key)

def selector(dictionary, id, value=None, force_write=False, debug=False):
    """
    Lee o escribe en un diccionario utilizando un identificador de selector. La función decide si leer o escribir
    basándose en la presencia del valor y la bandera de escritura forzada.

    Args:
        dictionary (dict): El diccionario objetivo para leer o escribir.
        id (str): Identificador del selector para leer o escribir en el diccionario.
        value: El valor a escribir en el diccionario. Si es None, se realiza una lectura.
        force_write (bool): Si es True, fuerza la escritura del valor en el diccionario, incluso si value es None.
        debug (bool): Si es True, activa el modo de depuración que lanza excepciones en lugar de retornar None.

    Returns:
        Si se está leyendo, retorna el valor leído del diccionario. Donde cualquier valor vacío entregará None.
        Si se está escribiendo, retorna True si se logró escribir o False si no fue posible.
    """
    # si no hay ID, se entrega inmediatamente None
    # esto puede ocurrir porque puede venir de una configuración o un valor por defecto que sea None
    if id is None:
        return None

    # si hay un valor, es una escritura en el diccionario
    if value is not None or force_write:
        try:
            _selector_write(dictionary, id, value)
            return True
        except Exception as e:
            if debug:
                raise e
            else:
                return False

    # si no hay un valor, y no se forzó escribir, es una lectura del diccionario
    try:
        return _selector_read_all(dictionary, id)
    except Exception as e:
        if debug:
            raise e
        else:
            return None

# ------------------------------------------------------------------------------
# Funcionalidades del módulo (funciones "privadas")
# ------------------------------------------------------------------------------

def _selector_write(dictionary, id, value):
    """
    Escribe un valor en un diccionario utilizando un identificador de selector. El selector puede representar
    una ruta de claves anidadas dentro del diccionario.

    Args:
        dictionary (dict): El diccionario donde se escribirán los datos.
        id (str): El identificador del selector que especifica la ruta de clave en el diccionario.
        value: El valor a escribir en la ubicación especificada por el selector.

    Returns:
        None: Esta función no retorna un valor, pero modifica el diccionario proporcionado.
    """
    parts = id.split('.')
    n_parts = len(parts)

    # Itera a través de las partes del selector para llegar a la ubicación deseada en el diccionario
    for i, part in enumerate(parts):
        if i == n_parts - 1:
            dictionary[part] = value
        else:
            # Si la clave no existe, crea un nuevo diccionario en esa posición
            dictionary = dictionary.setdefault(part, {})

def _selector_read_all(dictionary, id):
    """
    Procesa un identificador de selector que puede estar compuesto por varios selectores o cadenas literales y devuelve
    el valor resultante. Esta función maneja cadenas literales, selectores anidados y operadores OR dentro del selector.

    Args:
        dictionary (dict): El diccionario de donde se extraen los datos.
        id (str): El identificador del selector, que puede incluir varios selectores y cadenas literales.

    Returns:
        El valor resultante de procesar el selector. Si el selector contiene operadores OR,
        devuelve el primer valor no vacío encontrado.
    """
    # Envolver el selector en paréntesis si no comienza con uno
    if not id.startswith('(') and not id.startswith('"'):
        id = '(' + id + ')'

    parts = _selector_id_get_parts(id)

    # Si solo hay una parte y no es un operador OR, devuelve el valor directamente
    if len(parts) == 1 and parts[0]['type'] != 'operator':
        part = parts[0]
        if part['type'] == 'selector':
            if '||' not in part['id']:
                return _selector_read(dictionary, part['id'])
        elif part['type'] == 'if':
            return _selector_read(dictionary, part['id'])
        elif part['type'] == 'string':
            return part['value']

    # Procesa múltiples partes o la presencia de un operador OR
    final_value = None
    for part in parts:
        if part['type'] == 'string':
            final_value = _concatenate_values(final_value, part['value'])
        elif part['type'] in ['selector', 'if']:
            # Se buscan posibles operadores OR y se procesan
            sub_selectors = part['id'].split('||')
            or_value_found = False
            for sub_selector in sub_selectors:
                value = _selector_read(dictionary, sub_selector)
                if value not in (None, ''):
                    final_value = _concatenate_values(final_value, value)
                    or_value_found = True
                    break
            # Si no se encontró un valor válido se usa el último valor encontrado
            # Este último valor podría ser None o ''
            if not or_value_found:
                # Si la parte del selector es de OR, y no se encontró valor, siempre se entregará None como resultado del OR
                if '||' in part['id']:
                    value = None
                # Se asigna el último valor encontrado (en caso de OR) o el único valor encontrado (en caso de "no" OR)
                final_value = _concatenate_values(final_value, value)
        elif part['type'] == 'operator' and part['value'] == 'or':
            if final_value is not None:
                break

    return final_value

def _concatenate_values(current_value, new_value):
    if current_value is None:
        return new_value
    elif isinstance(current_value, str):
        return current_value + str(new_value)
    else:
        return str(current_value) + str(new_value)

def _selector_id_get_parts(id):
    """
    Descompone un identificador de selector en sus componentes individuales, incluyendo el manejo del operador OR y IF ternario.
    Cada componente puede ser una cadena literal, un selector anidado, un segmento separado por el operador OR, o un IF ternario.

    Args:
        id (str): El identificador del selector que puede incluir selectores anidados, cadenas literales, operadores OR y IF ternario.

    Returns:
        list: Una lista de diccionarios, donde cada diccionario representa un componente del selector.
    """
    values = []
    start_index = 0
    in_selector = False
    in_string = False
    depth = 0

    for index, char in enumerate(id):
        if char == '(' and not in_string:
            depth += 1
            if not in_selector:
                in_selector = True
                start_index = index
        elif char == ')' and not in_string:
            depth -= 1
            if in_selector and depth == 0:
                in_selector = False
                selector_id = id[start_index + 1:index]
                if '?' in selector_id:
                    values.append({'type': 'if', 'id': selector_id})
                else:
                    values.append({'type': 'selector', 'id': selector_id})
                start_index = index + 1
        elif char == '"' and not in_selector:
            in_string = not in_string
            if not in_string:
                values.append({'type': 'string', 'value': id[start_index + 1:index]})
                start_index = index + 1
        elif char == '|' and index < len(id) - 1 and id[index + 1] == '|' and not in_string and not in_selector and depth == 0:
            values.append({'type': 'operator', 'value': 'or'})
            start_index = index + 2

    return values

def _selector_read(dictionary, id):
    """
    Realiza una lectura recursiva en un diccionario utilizando un identificador de selector.
    Maneja tres tipos de selectores:
        - Selector simple: Valor directo desde una clave del diccionario.
        - Selector dependiente: Valor basado en una clave que depende de otro valor en el mismo diccionario.
        - Selector de arreglo: Valor desde un índice específico en un arreglo.
        - Selector de IF ternario: Valor que se elige de otro selector según una condición.
    Además, si hay cadenas literales pasadas como strings, las retornará directamente.
    La función se llama recursivamente para manejar selectores anidados.

    Args:
        dictionary: El diccionario de donde se extraen los datos.
        id: El identificador del selector.

    Returns:
        El valor correspondiente al selector o None si no se encuentra.
    """
    id = id.strip()
    if id == '':
        return dictionary

    # id mal formado (no puede terminar con .)
    if id.endswith('.'):
        return None

    # Cadena literal (no es un selector propiamente tal, se retorna tal cual sin comillas)
    if id.startswith('"') and id.endswith('"'):
        return id.strip('"')

    # procesar como un selector propio
    parts = id.split('.', 1)
    part = parts[0]
    next_id = parts[1] if len(parts) > 1 else ''

    # Selector simple: Valor obtenido directamente desde una clave del diccionario
    match_simple = re.fullmatch(r'^(\w+)$', part)
    if match_simple:
        return _selector_read_simple(dictionary, match_simple.group(1), next_id)

    # Selector dependiente: Valor en un diccionario que depende de otra clave
    match_dependent = re.fullmatch(r'^(\w+)\[(\w+)=([\w\s\-]+):(\w+)\]$', part)
    if match_dependent:
        return _selector_read_dependent(dictionary, *match_dependent.groups(), next_id)

    # Selector de arreglo: Valor de un arreglo en una clave específica
    match_array = re.fullmatch(r'^(\w+)\[(\d+)\]$', part)
    if match_array:
        return _selector_read_array(dictionary, *match_array.groups(), next_id)

    # Selector de IF ternario: con operador genérico
    match_if = re.fullmatch(r'\((.+?)\)\s*(\S+)\s*\"(.*?)\"\s*\?\s*\((.+?)\)\s*:\s*\((.+?)\)', id)
    if match_if:
        return _selector_read_if(dictionary, *match_if.groups())

    # Detectar si el ID es una expresión JSONPath
    if id.startswith("$."):
        return _selector_read_jsonpath(dictionary, id)

    # Detectar si el ID es una expresión JMESPath
    if id.startswith("jmespath:"):
        return _selector_read_jmespath(dictionary, id)

    # No se logró procesar el selector solicitado
    return None

def _selector_read_simple(dictionary, key, next_id):
    value = dictionary.get(key)
    return _selector_read(value, next_id) if isinstance(value, dict) and next_id else value

def _selector_read_dependent(dictionary, dictionary_key, required_key, required_value, dependent_key, next_id):
    array_list = dictionary.get(dictionary_key, [])
    for element in array_list:
        if str(element.get(required_key)) == str(required_value) and dependent_key in element:
            value = element[dependent_key]
            return _selector_read(value, next_id) if isinstance(value, dict) and next_id else value
    return None

def _selector_read_array(dictionary, array_key, array_index, next_id):
    array = dictionary.get(array_key, [])
    if isinstance(array, list) and len(array) > int(array_index):
        value = array[int(array_index)]
        return _selector_read(value, next_id) if isinstance(value, dict) and next_id else value
    return None

def _selector_read_if(dictionary, condition_selector, operator, value, true_selector, false_selector):
    condition_value = _selector_read_all(dictionary, condition_selector)
    try:
        true_or_false = _if_evaluate_condition(condition_value, operator.strip(), value.strip('"'))
    except ValueError:
        return None
    if true_or_false:
        return _selector_read_all(dictionary, true_selector)
    else:
        return _selector_read_all(dictionary, false_selector)

def _if_evaluate_condition(value_a, operator, value_b):
    # igualdad
    if operator in ('=', '=='):
        return str(value_a) == str(value_b)
    # desigualdad
    elif operator in ('!=', '<>'):
        return str(value_a) != str(value_b)
    # mayor
    elif operator == '>':
        return str(value_a) > str(value_b)
    # mayor igual
    elif operator == '>=':
        return str(value_a) >= str(value_b)
    # menor
    elif operator == '<':
        return str(value_a) < str(value_b)
    # menor igual
    elif operator == '<=':
        return str(value_a) <= str(value_b)
    # Contiene (para listas y strings)
    elif operator == 'contains':
        if isinstance(value_a, list):
            return value_b in [str(item) for item in value_a]
        else:
            return value_b in str(value_a)
    # Longitud (para strings y listas)
    elif operator == 'length':
        if isinstance(value_a, (list, str)):
            return len(value_a) == int(value_b)
    # Operador "es algo"
    elif operator == 'is':
        if value_b == 'None':
            return value_a is None
        elif value_b == 'not None':
            return value_a is not None
    # error en el caso de un operador no soportado
    raise ValueError(f"Operador no soportado: {operator}")

def _selector_read_jsonpath(dictionary, query):
    result = jsonpath(dictionary, query)
    # jsonpath.jsonpath retorna False si no encuentra coincidencias
    if result is False:
        return None
    # Manejar casos donde el resultado es una lista con un solo elemento
    if isinstance(result, list) and len(result) == 1:
        return result[0]
    return result

def _selector_read_jmespath(dictionary, query):
    query = query.replace("jmespath:", "", 1)
    result = jmespath.search(query, dictionary)
    if result is None or (isinstance(result, list) and not result):
        return None
    if isinstance(result, list) and len(result) == 1:
        return result[0]
    return result

# ------------------------------------------------------------------------------
# Casos de prueba
# ------------------------------------------------------------------------------

# Casos de prueba para dictionary_read_case_insensitive()
def test_dictionary_read_case_insensitive():
    test_dictionary = {'TeStKeY': 'TestValue'}
    assert dictionary_read_case_insensitive(test_dictionary, 'testkey') == 'TestValue'
    assert dictionary_read_case_insensitive(test_dictionary, 'unknown') is None

# Casos de prueba para selector de escritura que usa _selector_write
def test_selector_write(write_data, write_test):
    for test_case in write_test:
        selector_id = test_case['selector']
        value_to_write = test_case['value']
        expected_data = test_case['expected']
        selector(write_data, selector_id, value_to_write, debug=True)
        assert write_data == expected_data, \
            f"Error en selector_write con ID '{selector_id}': Datos esperados '{expected_data}', datos obtenidos '{write_data}'"

# Casos de prueba para selector de lectura que usa
def test_selector_read(read_data, read_test):
    for key, expected_value in read_test.items():
        real_value = selector(read_data, key, debug=True)
        assert real_value == expected_value, \
            f"Error en selector_read con ID '{key}': Valor esperado '{expected_value}' (tipo: {type(expected_value).__name__}), valor obtenido '{real_value}' (tipo: {type(real_value).__name__})"

# Ejecutar sólo si el módulo se llama directamente
if __name__ == '__main__':

    # Diccionario vacío, ya que acá se escribirán los datos de las pruebas de escritura
    write_data = {}

    # Casos de prueba con los resultados esperados las escrituras del selector
    write_test = [
        {'selector': 'new.key', 'value': 123, 'expected': {'new': {'key': 123}}},
        {'selector': 'new.key2', 'value': 'value', 'expected': {'new': {'key': 123, 'key2': 'value'}}}
    ]

    # Diccionario con datos para los casos de pruebas de lectura
    read_data = {
        'zero': 0,
        'k_simple': 'v_simple',
        'k_nested1': {
            'k_nested2': 'v_nested'
        },
        'k_nested1p': {
            'k_nested2p': {
                'k_nested3p': 'v_nested'
            }
        },
        'array': [1, 2, 3],
        'nested_array': {
            'array': [1, 2, 3]
        },
        'mixed': [
            {
                'key': 10,
                'value': 'hola'
            },
            {
                'key': 20,
                'value': 'mundo'
            },
            {
                'key': 30,
                'value': 'chao'
            },
        ],
        'nested_mixed': {
            'mixed': [
                {
                    'key': 10,
                    'value': 'hola'
                },
            ]
        },
        'mixed_with_childs': [
            {
                'key': 20,
                'child': {
                    'value': 'hijo'
                }
            }
        ],
        'mixed_dash': [
            {
                'key': 'key-1',
                'value': 'value-1'
            }
        ],
        'selector_or': {
            'k1': None,
            'k2': '',
            'k3': 'v3',
            'k4': 'v4',
        }
    }

    # Casos de prueba con los resultados esperados las lecturas del selector
    read_test = {
        # Casos sin OR
        'zero': 0,
        'k_simple': 'v_simple',
        'k_nested1.k_nested2': 'v_nested',
        'k_nested1p.k_nested2p.k_nested3p': 'v_nested',
        'array[1]': 2,
        'nested_array.array': [1, 2, 3],
        'nested_array.array[2]': 3,
        'nested_array.array2[2]': None, # Caso que no existe
        'nested_array.array[0]': 1,
        'mixed[key=20:value]': 'mundo',
        'mixed2[key=20:value]': None, # Caso que no existe
        'mixed_dash[key=key-1:value]': 'value-1',
        'nested_mixed.mixed[key=10:value]': 'hola',
        'mixed_with_childs[key=20:child].value': 'hijo',
        '(k_simple)': 'v_simple',
        '"k_simple"': 'k_simple',
        '(k_simple)(k_simple)': 'v_simplev_simple',
        '"("(k_simple)")"': '(v_simple)',
        '(k_simple)"k_simple"': 'v_simplek_simple',
        '"k_simple"(k_simple)': 'k_simplev_simple',
        '(k_simple)"k_simple""k_simple"': 'v_simplek_simplek_simple',
        '"k_simple"(k_simple)(k_simple)': 'k_simplev_simplev_simple',
        '"k_simple"(k_simple)"k_simple"': 'k_simplev_simplek_simple',
        '(k_simple)"k_simple"(k_simple)': 'v_simplek_simplev_simple',
        '"Forma de pago: "(k_nested1.k_nested2)': 'Forma de pago: v_nested',
        '"Forma de pago: "(k_nested1.k_nested2)" / checkout_id: "(mixed_with_childs[key=20:child].value)': 'Forma de pago: v_nested / checkout_id: hijo',
        # Casos con OR
        'k_empty||k_simple': 'v_simple',
        'k_empty||"cadena literal"': 'cadena literal',
        '"val: "(k_simple)||" y "(k_nested1.k_nested2)': 'val: v_simple',
        'selector_or.k1||selector_or.k2||selector_or.k3': 'v3',
        '"Hola"||"Mundo"': 'Hola',
        '"Hola"||k_simple': 'Hola',
        'k_simple||"Hola"': 'v_simple',
        '"Valor: "(k_simple||"Sin valor")': 'Valor: v_simple',
        '"Valor: "(k_simple_bad||"Sin valor")': 'Valor: Sin valor',
        '"Valor: "(k_simple||"Sin valor")||"Valor por defecto"': 'Valor: v_simple',
        '(k_simple_bad||"")||"Valor por defecto"': 'Valor por defecto',
        # Casos con IF ternario
        '((k_simple) = "v_simple" ? (k_nested1.k_nested2) : (array[1]))': 'v_nested',
        '((k_simple) != "no_v_simple" ? (k_nested1.k_nested2) : (array[1]))': 'v_nested',
        '((array[2]) > "2" ? (nested_array.array[1]) : (nested_array.array[2]))': 2,
        '((array[1]) < "2" ? (nested_array.array[0]) : (nested_array.array[2]))': 3,
        '((mixed_with_childs[key=20:child].value) == "hijo" ? ("V") : ("F"))': 'V',
        '((array) contains "2" ? ("Sí") : ("No"))': 'Sí',
        '((k_simple) contains "simple" ? ("Sí") : ("No"))': 'Sí',
        '((array) length "3" ? ("Sí") : ("No"))': 'Sí',
        '((k_simple) length "8" ? ("Sí") : ("No"))': 'Sí',  # Longitud de 'v_simple' es 8
        '((k_nested1.k_nested2) length "7" ? ("Sí") : ("No"))': 'No',  # Longitud de 'v_nested' es 8
        # Casos con IF ternario y operador OR en selector
        '((k_empty||"cadena literal") = "cadena literal" ? ("String") : ("Valor de k_empty"))': 'String',
    }

    # actualización de read_data y read_test para pruebas unitarias más complejas
    read_data.update({
        'complex_dict': {
            'nested': {
                'key1': 'value1',
                'key2': 2,
                'key3': [1, 2, 3]
            },
            'list_of_dicts': [
                {'item_key': 'item_value1'},
                {'item_key': 'item_value2'}
            ]
        },
        'bool_value': True,
        'numeric_value': 42,
        'empty_string': '',
        'null_value': None,
        'false_value': False,
        'list_with_mixed_types': ['text', 123, True, None],
    })
    read_test.update({
        # Pruebas con Diccionarios Anidados
        'complex_dict.nested.key1': 'value1',
        'complex_dict.nested.key2': 2,
        'complex_dict.nested.key3[1]': 2,
        # Pruebas con Listas de Diccionarios
        'complex_dict.list_of_dicts[0].item_key': 'item_value1',
        'complex_dict.list_of_dicts[1].item_key': 'item_value2',
        # Pruebas de Error
        'complex_dict.non_existent_key': None, # Selector no válido
        'complex_dict.': None, # Selector vacío
        'complex_dict..nested': None, # Selector mal formado
        'complex_dict.invalid..key': None, # Selector doblemente mal formado
        # Pruebas con Diversos Tipos de Datos
        'numeric_value': 42,
        'empty_string': '',
        'bool_value': True,
        'false_value': False,
        'null_value': None,
        # Casos donde se concatena con diversos tipos de datos (los de arriba)
        '"numeric_value: "(numeric_value)': 'numeric_value: 42',
        '"empty_string: "(empty_string)': 'empty_string: ',
        '"bool_value: "(bool_value)': 'bool_value: True',
        '"false_value: "(false_value)': 'false_value: False',
        '"null_value: "(null_value)': 'null_value: None',
        # Casos con operador OR usando campos vacío
        'null_value||null_value': None,
        'empty_string||empty_string': None, # Un OR entregará None si todos los selectores son None o '' (string vacío)
        'null_value||"NONE"': 'NONE',
        'empty_string||"EMPTY"': 'EMPTY',
        'false_value||"FALSE"': False, # False no tiene valor por defecto, ya que si tiene valor, es False.
        # Casos con campos vacíos en Operadores ID
        '((null_value) is "None" ? ("null_value es null") : ("null_value no es null"))': 'null_value es null',
        # Casos de Borde con Operadores IF
        '((numeric_value) > "41" ? ("Mayor a 41") : ("Menor o igual a 41"))': 'Mayor a 41',
        '((bool_value) == "True" ? ("Verdadero") : ("Falso"))': 'Verdadero',
        '((empty_string) == "" ? ("Cadena vacía") : ("Cadena no vacía"))': 'Cadena vacía',
        # Prueba con lista mixta
        'list_with_mixed_types[0]': 'text',
        'list_with_mixed_types[1]': 123,
        'list_with_mixed_types[2]': True,
        'list_with_mixed_types[3]': None,
    })

    # actualización de read_test para probar casos con JSONPath
    read_test.update({
        # Acceso Directo a una Clave en Primer Nivel
        "$.k_simple": "v_simple",
        # Acceso a un Elemento Anidado
        "$.k_nested1.k_nested2": "v_nested",
        # Acceso a un Elemento de un Arreglo por Índice
        "$.array[1]": 2,
        # Acceso a un Elemento Anidado Dentro de un Arreglo
        "$.nested_array.array[2]": 3,
        # Filtrar Elementos de un Arreglo (por valor existente)
        "$.mixed[?(@.key == 20)].value": "mundo",
        # Filtrar Elementos de un Arreglo (resultado vacío)
        "$.mixed[?(@.key == 999)]": None,
        # Acceso a Todos los Elementos de un Arreglo
        "$.array[*]": [1, 2, 3],
        # Obtener Elementos Basados en una Condición Compleja
        "$.mixed[?(@.key > 15)].value": ["mundo", "chao"],
        # Obtener un Elemento Anidado en un Diccionario dentro de un Arreglo
        "$.mixed_with_childs[?(@.key == 20)].child.value": "hijo",
        # Caso adicional (acceso a un elemento booleano)
        "$.bool_value": True,
    })

    # actualización de read_test para probar casos con JSONPath mezclados con los selectores originales
    read_test.update({
        # Acceso Directo y Concatenación de Texto
        '"k_simple: "($.k_simple)': 'k_simple: v_simple',
        # Selección con OR y JSONPath
        '($.k_simple_bad)||($.k_simple)': 'v_simple',
        # Valor por Defecto con OR y JSONPath
        '($.k_simple_bad)||"Valor por defecto"': 'Valor por defecto',
        # Condición con IF Ternario y JSONPath
        '((($.k_simple_bad)||($.k_simple)) == "v_simple" ? ("V") : ("F")))': 'V',
        # Concatenación con Valor de un Arreglo
        '"array[0]: "($.array[0])': 'array[0]: 1',
        # Filtrado de Arreglo y Concatenación
        '"Elementos > 1 en array: " + str($.array[?(@ > 1)])': 'Elementos > 1 en array: [2, 3]',
        # Acceso a Elemento Anidado y Concatenación
        '"nested_array.array[2]: "($.nested_array.array[2])': 'nested_array.array[2]: 3',
        # Filtrado de Arreglo de Diccionarios y Concatenación
        '"mixed[key=20:value]: "($.mixed[?(@.key == 20)].value)': 'mixed[key=20:value]: mundo',
        # Concatenación de un valor extraído del arreglo con texto
        '"Primer valor en mixed: "($.mixed[0].value)': 'Primer valor en mixed: hola',
        # Acceder a un valor anidado y concatenar con un valor de un arreglo usando JSONPath
        '"Valor anidado y primer valor de array: "($.k_nested1.k_nested2)" y "($.array[0])': 'Valor anidado y primer valor de array: v_nested y 1',
    })

    # actualización de read_test para probar casos con JMESPath
    read_test.update({
        # Acceso Directo a una Clave en Primer Nivel
        "jmespath:k_simple": "v_simple",
        # Acceso a un Elemento Anidado
        "jmespath:k_nested1.k_nested2": "v_nested",
        # Acceso a un Elemento de un Arreglo por Índice
        "jmespath:array[1]": 2,
        # Acceso a un Elemento Anidado Dentro de un Arreglo
        "jmespath:nested_array.array[2]": 3,
        # Filtrar Elementos de un Arreglo (por valor existente)
        "jmespath:mixed[?key == `20`].value": "mundo",
        # Filtrar Elementos de un Arreglo (resultado vacío)
        "jmespath:mixed[?key == `999`]": None,
        # Acceso a Todos los Elementos de un Arreglo
        "jmespath:array[*]": [1, 2, 3],
        # Obtener Elementos Basados en una Condición Compleja
        "jmespath:mixed[?key > `15`].value": ["mundo", "chao"],
        # Obtener un Elemento Anidado en un Diccionario dentro de un Arreglo
        "jmespath:mixed_with_childs[?key == `20`].child.value": "hijo",
        # Caso adicional (acceso a un elemento booleano)
        "jmespath:bool_value": True,
    })

    # actualización de read_test para probar casos con JMESPath mezclados con los selectores originales
    read_test.update({
        # Acceso Directo y Concatenación de Texto
        '"k_simple: "(jmespath:k_simple)': 'k_simple: v_simple',
        # Selección con OR y JMESPath
        'jmespath:k_simple_bad||jmespath:k_simple': 'v_simple',
        # Valor por Defecto con OR y JMESPath
        'jmespath:k_simple_bad||"Valor por defecto"': 'Valor por defecto',
        # Condición con IF Ternario y JMESPath
        '((jmespath:k_simple_bad||jmespath:k_simple) == "v_simple" ? ("V") : ("F")))': 'V',
        # Concatenación con Valor de un Arreglo
        '"array[0]: "(jmespath:array[0])': 'array[0]: 1',
        # Filtrado de Arreglo y Concatenación
        '"Elementos > 1 en array: "(jmespath:array[? @ > `1`])': 'Elementos > 1 en array: [2, 3]',
        # Acceso a Elemento Anidado y Concatenación
        '"nested_array.array[2]: "(jmespath:nested_array.array[2])': 'nested_array.array[2]: 3',
        # Filtrado de Arreglo de Diccionarios y Concatenación
        '"mixed[key=20:value]: "(jmespath:mixed[?key == `20`].value)': 'mixed[key=20:value]: mundo',
        # Concatenación de un valor extraído del arreglo con texto
        '"Primer valor en mixed: "(jmespath:mixed[0].value)': 'Primer valor en mixed: hola',
        # Acceder a un valor anidado y concatenar con un valor de un arreglo usando JMESPath
        '"Valor anidado y primer valor de array: "(jmespath:k_nested1.k_nested2)" y "(jmespath:array[0])': 'Valor anidado y primer valor de array: v_nested y 1',
    })

    # Ejecutar los casos de prueba
    try:
        test_dictionary_read_case_insensitive()
        test_selector_read(read_data, read_test)
        test_selector_write(write_data, write_test)
        print("Todos los casos de prueba pasaron.")
    except (Exception, AssertionError) as e:
        # Mostrar el JSON de las pruebas de lectura
        from json import dumps
        print('read_data = ' + dumps(read_data))
        print('='*80)
        # Mostrar error "bonito"
        print("Ocurrió un error:", type(e).__name__, "-", e)
