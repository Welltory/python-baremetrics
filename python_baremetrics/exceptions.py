# -*- coding: utf-8 -*-


class BaremetricsException(Exception):
    pass


class APICallNotImplemented(BaremetricsException):
    pass


class BaremetricsAPIException(BaremetricsException):
    def __init__(self, r_message):
        message = '[{}] {} {}'.format(
            r_message.status_code,
            r_message.request.method,
            r_message.request.url,
        )
        super(BaremetricsAPIException, self).__init__(message)
