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
import inspect
from datetime import datetime

# clase que representa un mensaje dentro del log
class LogMessage:
    log_format = '%(created)s %(category)s %(level_name)s: %(message)s [%(module)s:%(line_number)s]'

    def __init__(self, level, message, args = {}, category = None, data = None):
        # datos del mensaje del log
        self.created = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.category = category if category is not None else 'general'
        self.level = level
        self.message = message
        self.args = args
        self.data = data
        # agregar los datos del que llamó al log
        caller_frame = inspect.currentframe().f_back.f_back.f_back
        filename, line_number, function_name, lines, index = inspect.getframeinfo(caller_frame)
        mod = inspect.getmodule(caller_frame)
        self.module = mod.__name__
        self.filename = filename
        self.line_number = line_number
        self.function_name = function_name

    @property
    def level_name(self):
        levels = {
            10: 'DEBUG',
            20: 'INFO',
            30: 'WARNING',
            40: 'ERROR',
            50: 'CRITICAL',
        }
        return levels[int(self.level)]

    def to_dict(self):
        return {
            'created': self.created,
            'category': self.category,
            'level': self.level,
            'level_name': self.level_name,
            'message': self.message,
            'args': self.args,
            'data': self.data,
            'module': self.module,
            'filename': self.filename,
            'line_number': self.line_number,
            'function_name': self.function_name,
        }

    def __str__(self):
        return self.log_format % self.to_dict()

# clase con el log basado en memoria (almacena el log en una lista)
class MemoryLogging:
    # levels (severities)
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

    def __init__(self, level = None, category = None):
        self.__logs = []
        self.logging_level = level if level is not None else MemoryLogging.INFO
        self.default_category = category

    def __write(self, level, message, args, category, data):
        if category is None:
            category = self.default_category
        log_message = LogMessage(level, message, args, category, data)
        if level >= self.logging_level:
            self.__logs.append(log_message)
        return log_message

    def debug(self, message, args = None, category = None, data = None):
        return self.__write(MemoryLogging.DEBUG, message, args, category, data)

    def info(self, message, args = None, category = None, data = None):
        return self.__write(MemoryLogging.INFO, message, args, category, data)

    def warning(self, message, args = None, category = None, data = None):
        return self.__write(MemoryLogging.WARNING, message, args, category, data)

    def error(self, message, args = None, category = None, data = None):
        return self.__write(MemoryLogging.ERROR, message, args, category, data)

    def critical(self, message, args = None, category = None, data = None):
        return self.__write(MemoryLogging.CRITICAL, message, args, category, data)

    def get_all(self, as_dict = False):
        if as_dict:
            return list(map(lambda x: x.to_dict(), self.__logs))
        return self.__logs

    def flush(self, as_dict = False):
        logs = self.get_all(as_dict)
        self.__logs = []
        return logs

# ------------------------------------------------------------------------------
# Caso de prueba
# ------------------------------------------------------------------------------

if __name__ == '__main__':

    # crear log
    logging = MemoryLogging()
    #logging = MemoryLogging(MemoryLogging.DEBUG)

    # registrar un log de cada nivel
    logging.debug('A Debug Logging Message') # no se agrega por nivel por defecto
    logging.info('A Info Logging Message')
    logging.warning('A Warning Logging Message')
    logging.error('An Error Logging Message')
    logging.critical('A Critical Logging Message')

    # obtener los logs e imprimirlos
    logs = logging.get_all()
    for log in logs:
        print(str(log))
