# -*- coding: utf-8 -*-


class BaremetricsException(Exception):
    pass


class APICallNotImplemented(BaremetricsException):
    pass


class BaremetricsAPIException(BaremetricsException):
    def __init__(self, r_message):
        message = 'Got [{}] "{}" when calling {} {}'.format(
            r_message.status_code,
            r_message.json().get('error'),
            r_message.request.method,
            r_message.request.url,
        )
        super(BaremetricsAPIException, self).__init__(message)
